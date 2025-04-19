import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import io
from datetime import datetime

# Cargar las variables de entorno desde el archivo .env si estamos en local
load_dotenv()

# Verificar si estamos en Streamlit Cloud o en local
if "MONGODB_URI" in os.environ:
    # Si estamos en local, cargar desde el archivo .env
    MONGODB_URI = os.getenv("MONGODB_URI")
else:
    # Si estamos en Streamlit Cloud, cargar desde st.secrets
    MONGODB_URI = st.secrets["MONGODB_URI"]

# Conexión a MongoDB
client = MongoClient(MONGODB_URI)
db = client["asistente_db"]
coleccion = db["videos"]

# Ejemplo de guardar datos en MongoDB
def guardar_en_mongo(titulo, url, transcripcion, pdf_bytes):
    video_doc = {
        "titulo": titulo,
        "url": url,
        "transcripcion": transcripcion,
        "pdf": pdf_bytes,
        "fecha_creacion": datetime.now()
    }

    result = coleccion.insert_one(video_doc)
    return result.inserted_id
