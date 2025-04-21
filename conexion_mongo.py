# conexion_mongo.py
import os  # Importa el módulo os para interactuar con el sistema operativo.
import streamlit as st  # Importa Streamlit para manejar secretos y la interfaz.
from pymongo import MongoClient  # Importa MongoClient para conectarse a MongoDB.
from dotenv import load_dotenv  # Importa load_dotenv para cargar variables de entorno desde un archivo .env.
import io  # Importa io para manejar datos en memoria.
from datetime import datetime  # Importa datetime para trabajar con fechas y horas.

# Cargar las variables de entorno desde el archivo .env si estamos en local.
load_dotenv()

# Verificar si estamos en Streamlit Cloud o en local.
if "MONGODB_URI" in os.environ:
    # Si estamos en local, cargar la URI de MongoDB desde el archivo .env.
    MONGODB_URI = os.getenv("MONGODB_URI")
else:
    # Si estamos en Streamlit Cloud, cargar la URI de MongoDB desde st.secrets.
    MONGODB_URI = st.secrets["MONGODB_URI"]

# Conexión a MongoDB.
# Crea un cliente de MongoDB utilizando la URI proporcionada.
client = MongoClient(MONGODB_URI)

# Selecciona la base de datos "asistente_db".
db = client["asistente_db"]

# Selecciona la colección "videos" dentro de la base de datos.
coleccion = db["videos"]

# Función para guardar datos en MongoDB.
def guardar_en_mongo(titulo, url, transcripcion, pdf_bytes):
    """
    Guarda un documento en la colección de MongoDB.

    Args:
        titulo (str): El título del video.
        url (str): La URL del video.
        transcripcion (str): La transcripción del video.
        pdf_bytes (bytes): Los datos del PDF en formato binario.
    
    Returns:
        ObjectId: El ID del documento insertado en la colección.
    """
    # Crea un documento con los datos proporcionados.
    video_doc = {
        "titulo": titulo,  # Título del video.
        "url": url,  # URL del video.
        "transcripcion": transcripcion,  # Transcripción del video.
        "pdf": pdf_bytes,  # PDF en formato binario.
        "fecha_creacion": datetime.now()  # Fecha y hora de creación del documento.
    }

    # Inserta el documento en la colección y devuelve el ID del documento insertado.
    result = coleccion.insert_one(video_doc)
    return result.inserted_id