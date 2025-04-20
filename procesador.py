import os
import tempfile
from datetime import datetime
from fpdf import FPDF
import torch
import yt_dlp
import re
from dotenv import load_dotenv
import io  
from conexion_mongo import guardar_en_mongo

# Cargar variables de entorno
load_dotenv()

def procesar_video(url):
    import whisper  # Cargar whisper solo cuando se use la función

    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, 'video.%(ext)s')

    # Ruta al archivo de cookies exportado desde el navegador
    cookies_path = os.path.join(os.getcwd(), 'cookies', 'cookies.txt')
  # Actualiza esto según la ubicación de tus cookies

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'noplaylist': True,
        'cookies': cookies_path,  # Usa las cookies para autenticar
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            titulo = info.get('title', 'Video sin título')
        except yt_dlp.utils.DownloadError as e:
            print(f"Error descargando el video: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    audio_file = os.path.join(temp_dir, 'video.mp3')

    # Transcribir con Whisper
    model_whisper = whisper.load_model("base")  # Solo se carga cuando se usa
    resultado = model_whisper.transcribe(audio_file)
    transcripcion = resultado['text']

    # Limpiar el texto para almacenamiento seguro
    transcripcion_limpia = transcripcion.encode('latin-1', 'replace').decode('latin-1')
    titulo_limpio = titulo.encode('latin-1', 'replace').decode('latin-1')

    # Crear PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Título: {titulo_limpio}\n\nTranscripción:\n{transcripcion_limpia}")

    # Exportar el PDF a bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Guardar en MongoDB y obtener el ID
    video_id = guardar_en_mongo(titulo_limpio, url, transcripcion_limpia, pdf_bytes)

    return {
        'titulo': titulo_limpio,
        'transcripcion': transcripcion_limpia,
        'id': str(video_id)  # Incluye el id del video
    }

def responder_pregunta(pregunta, transcripcion, max_chars=500):
    from transformers import T5Tokenizer, T5ForConditionalGeneration  # Cargar solo cuando se necesite

    # Cargar el modelo y tokenizador T5 cuando se llama la función
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")

    respuestas = []

    for i in range(0, len(transcripcion), max_chars):
        fragmento = transcripcion[i:i+max_chars]
        if fragmento.strip():
            try:
                input_text = f"question: {pregunta} context: {fragmento}"
                inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
                outputs = model.generate(inputs['input_ids'], max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
                respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
                respuestas.append(respuesta)
            except Exception as e:
                print(f"Error procesando fragmento: {e}")

    if not respuestas:
        return "No se pudo generar una respuesta con el modelo."

    return " ".join(respuestas)
