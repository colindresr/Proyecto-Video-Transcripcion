# videos/api_urls.py
from django.urls import path
from .api import procesar, preguntar, descargar_pdf  # ✅ Aquí importas la vista

urlpatterns = [
    path("procesar/", procesar),
    path("preguntar/", preguntar),
    path("descargar_pdf/", descargar_pdf),
]
