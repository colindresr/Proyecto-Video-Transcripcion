# videos/urls.py

from django.urls import path  # Importa la función path para definir rutas de URL.
from .api import procesar_video, preguntar, descargar_pdf  # Importa las vistas que manejarán las solicitudes.

# Definición de las rutas de la aplicación.
urlpatterns = [
    path("procesar/", procesar_video),  # Ruta para procesar un video.
    path("preguntar/", preguntar),  # Ruta para realizar preguntas sobre un video.
    path("descargar_pdf/", descargar_pdf),  # Ruta para descargar la transcripción en formato PDF.
]