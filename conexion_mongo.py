import os
from pymongo import MongoClient
from dotenv import load_dotenv
from fpdf import FPDF
import io
from datetime import datetime 

# Cargar variables de entorno desde el .env
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["asistente_db"]

coleccion = db["videos"]

def guardar_en_mongo(titulo, url, transcripcion, pdf_bytes):
    video_doc = {
        "titulo": titulo,
        "url": url,
        "transcripcion": transcripcion,
        "pdf": pdf_bytes,
        "fecha_creacion": datetime.now(),
    }

    result = coleccion.insert_one(video_doc)  # Inserta el documento
    return result.inserted_id  # Devuelve el id del documento insertado
