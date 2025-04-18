# videos/api_urls.py
from django.urls import path
from .api import procesar_video, preguntar, descargar_pdf  # ✅ Aquí importas la vista

urlpatterns = [
    path("procesar/", procesar_video),
    path("preguntar/", preguntar),
    path("descargar_pdf/", descargar_pdf),  # ✅ Ruta ya puede registrar la vista correctamente
]
