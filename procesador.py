# procesador.py
import os  # Importa el módulo os para interactuar con el sistema operativo.
import tempfile  # Importa tempfile para crear archivos y directorios temporales.
from datetime import datetime  # Importa datetime para trabajar con fechas y horas.
from fpdf import FPDF  # Importa FPDF para generar archivos PDF.
import torch  # Importa PyTorch para tareas relacionadas con modelos de aprendizaje profundo.
import yt_dlp  # Importa yt-dlp para descargar videos y audios de plataformas como YouTube.
import re  # Importa re para trabajar con expresiones regulares.
from dotenv import load_dotenv  # Importa load_dotenv para cargar variables de entorno desde un archivo .env.
import io  # Importa io para manejar datos en memoria.
from conexion_mongo import guardar_en_mongo  # Importa la función para guardar datos en MongoDB.
from duckduckgo_search import DDGS

# Cargar variables de entorno
load_dotenv()


# Verifica que DJANGO_API_URL esté configurada correctamente
DJANGO_API_URL = os.getenv("DJANGO_API_URL")
print(f"DJANGO_API_URL: {DJANGO_API_URL}")  # Esto debería imprimir "http://localhost:10000" si está configurado correctamente

is_local = os.getenv("DJANGO_API_URL", "").startswith("http://localhost")

def escribir_cookies_temporales():
    """
    Escribe las cookies necesarias para yt-dlp en un archivo temporal.

    Returns:
        str: La ruta al archivo temporal de cookies.
    """
    cookies_data = os.getenv("YTDLP_COOKIES")
    if not cookies_data:
        raise ValueError("No se encontró la variable YTDLP_COOKIES")

    temp_dir = tempfile.mkdtemp()
    cookies_path = os.path.join(temp_dir, "cookies.txt")

    # Guardar las cookies en el archivo temporal
    with open(cookies_path, "w", encoding="utf-8") as f:
        f.write(cookies_data)

    return cookies_path

def procesar_video(url):
    """
    Procesa un video desde una URL, transcribe su contenido y lo guarda en MongoDB.

    Args:
        url (str): La URL del video a procesar.

    Returns:
        dict: Un diccionario con el título, la transcripción y el ID del video en MongoDB, o un error.
    """
    import whisper  # Importa Whisper solo cuando se necesita.

    temp_dir = tempfile.mkdtemp()  # Crea un directorio temporal para almacenar archivos.
    output_path = os.path.join(temp_dir, 'video.%(ext)s')  # Ruta para guardar el archivo descargado.

    # Verifica si estás en un entorno local
    is_local = os.getenv("DJANGO_API_URL", "").startswith("http://localhost")

    # Configuración de cookies (solo si no estás en local)
    cookies_path = None
    if not is_local:
        try:
            cookies_path = escribir_cookies_temporales()  # Genera el archivo de cookies temporales.
        except Exception as e:
            print(f"Error generando cookies temporales: {e}")
            return {'error': f"Error generando cookies temporales: {str(e)}"}

    # Configuración de yt-dlp para descargar el video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Agrega las cookies si no estás en local
    if cookies_path:
        ydl_opts['cookies'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)  # Descarga el video y obtiene su información.
            titulo = info.get('title', 'Video sin título')  # Obtiene el título del video.
        except yt_dlp.utils.DownloadError as e:
            print(f"Error descargando el video: {e}")
            return {'error': f"Error descargando el video: {str(e)}"}
        except Exception as e:
            print(f"Error inesperado: {e}")
            return {'error': f"Error inesperado: {str(e)}"}

    audio_file = os.path.join(temp_dir, 'video.mp3')  # Ruta del archivo de audio descargado.

    # Transcripción con Whisper.
    try:
        model_whisper = whisper.load_model("base")  # Carga el modelo Whisper.
        resultado = model_whisper.transcribe(audio_file)  # Transcribe el audio.
        transcripcion = resultado['text']
    except Exception as e:
        print(f"Error transcribiendo el video: {e}")
        return {'error': f"Error transcribiendo el video: {str(e)}"}

    # Limpiar el texto para almacenamiento seguro.
    transcripcion_limpia = transcripcion.encode('latin-1', 'replace').decode('latin-1')
    titulo_limpio = titulo.encode('latin-1', 'replace').decode('latin-1')

    # Crear PDF en memoria.
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Título: {titulo_limpio}\n\nTranscripción:\n{transcripcion_limpia}")
        pdf_bytes = pdf.output(dest='S').encode('latin1')
    except Exception as e:
        print(f"Error generando el PDF: {e}")
        return {'error': f"Error generando el PDF: {str(e)}"}

    # Guardar en MongoDB y obtener el ID.
    try:
        video_id = guardar_en_mongo(titulo_limpio, url, transcripcion_limpia, pdf_bytes)
    except Exception as e:
        print(f"Error guardando en MongoDB: {e}")
        return {'error': f"Error guardando en MongoDB: {str(e)}"}

    return {
        'titulo': titulo_limpio,
        'transcripcion': transcripcion_limpia,
        'id': str(video_id)
    }

def responder_pregunta(pregunta, transcripcion, max_chars=300):
    """
    Responde una pregunta basada en una transcripción utilizando un modelo T5.

    Args:
        pregunta (str): La pregunta a responder.
        transcripcion (str): El texto de la transcripción.
        max_chars (int): El tamaño máximo de los fragmentos de texto a procesar.

    Returns:
        str: La respuesta generada por el modelo.
    """
    from transformers import T5Tokenizer, T5ForConditionalGeneration

    # Cargar el modelo y el tokenizador
    tokenizer = T5Tokenizer.from_pretrained("t5-base", legacy=False)
    # Cargar el modelo T5 preentrenado
    model = T5ForConditionalGeneration.from_pretrained("t5-base")

    respuestas = []

    # Limpieza de la transcripción
    transcripcion = re.sub(r'\s+', ' ', transcripcion)  # Reemplaza múltiples espacios por uno solo
    transcripcion = re.sub(r'[^\w\s.,!?]', '', transcripcion)  # Elimina caracteres no deseados

    # Divide la transcripción en fragmentos y procesa cada uno
    for i in range(0, len(transcripcion), max_chars):
        fragmento = transcripcion[i:i+max_chars]
        if fragmento.strip():
            try:
                # Formato de entrada mejorado
                input_text = f"Resuma el siguiente texto de manera clara: {fragmento}"
                inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)

                # Generación de texto con hiperparámetros ajustados
                outputs = model.generate(
                    inputs['input_ids'],
                     max_length=75,  # Longitud máxima de la respuesta
                    do_sample=True,  # Habilita el muestreo
                    temperature=0.7,  # Controla la aleatoriedad
                    top_k=50,  # Limita a los 50 tokens más probables
                    top_p=0.9,  # Usa nucleus sampling
                    num_return_sequences=1,  # Genera una sola respuesta
                    no_repeat_ngram_size=2  # Evita repeticiones
                )

                # Decodifica la respuesta y la agrega a la lista
                respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
                respuestas.append(respuesta.strip())
            except Exception as e:
                print(f"Error procesando fragmento: {e}")

    if not respuestas:
        return "No se pudo generar una respuesta con el modelo."

    # Combina las respuestas y elimina redundancias
    respuesta_final = " ".join(respuestas)
    respuesta_final = re.sub(r'\s+', ' ', respuesta_final)  # Limpia espacios extra
    return respuesta_final

def buscar_en_internet(query, max_resultados=5, pregunta=None, transcripcion=None):
    """
    Realiza una búsqueda en Internet usando DuckDuckGo, con la opción de generar contexto usando responder_pregunta.

    Args:
        query (str): La consulta de búsqueda.
        max_resultados (int): Número máximo de resultados a devolver.
        pregunta (str): La pregunta para generar contexto.
        transcripcion (str): El texto de la transcripción para generar contexto.

    Returns:
        list: Una lista de diccionarios con 'titulo', 'url' y 'resumen' de los resultados.
    """
    resultados = []

    # Generar contexto si se proporciona una pregunta y una transcripción
    contexto = None
    if pregunta and transcripcion:
        contexto = responder_pregunta(pregunta, transcripcion)

    try:
        # Si hay contexto, lo agrega a la consulta
        if contexto:
            query = f"{query} {contexto}"

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_resultados):
                resultados.append({
                    'titulo': r.get('title'),
                    'url': r.get('href'),
                    'resumen': r.get('body')
                })
    except Exception as e:
        return [{'error': f"No se pudo realizar la búsqueda: {str(e)}"}]

    return resultados