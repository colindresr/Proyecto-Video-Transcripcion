#  Asistente de Transcripción de Videos

Este proyecto es una aplicación web que permite transcribir videos de YouTube, guardar la transcripción en PDF y hacer preguntas sobre el contenido del video. Está desarrollado con **Streamlit** como frontend, **Django REST Framework** como backend, y usa **MongoDB** para almacenar los datos.

---

##  Funcionalidades

- Subida de links de videos de YouTube o archivos `.txt` con múltiples enlaces.
- Transcripción automática de audio (con Whisper).
- Generación y almacenamiento de transcripción en formato PDF.
- Preguntas y respuestas sobre el contenido del video (usando un modelo LLM).
- Almacenamiento de PDFs y transcripciones en MongoDB.
- Navegación sencilla entre secciones (`Inicio` y `Chat`) desde el frontend.

---

##  Tecnologías Usadas

### Backend
- [FFmpeg] para obtener audio
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytube](https://pytube.io/) / `yt-dlp` para descarga de videos
- [OpenAI Whisper](https://github.com/openai/whisper) para transcripción
- [FPDF](https://pymupdf.readthedocs.io/) para generación de PDFs
- [pymongo](https://pymongo.readthedocs.io/) para conexión a MongoDB
- [T5 Transformers] para Procesamiento de Lenguaje Natural e Inteligencia Artificial
- DuckDuckGo para realizar las búsquedas en internet

### Frontend
- [Streamlit](https://streamlit.io/)
- Estilizado con `styles.css`
- Navegación por secciones y subida de archivos

### Base de Datos
- [MongoDB Atlas](https://www.mongodb.com/atlas) para almacenamiento en la nube

---

## Configuración Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/colindresr/Proyecto-Video-Transcripcion.git
cd proyecto-video-transcripcion
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear un archivo `.env` en la raíz del proyecto y agregar las siguientes variables de entorno como en el archivo .env.example
```env
MONGODB_URI="URL de la base de datos MongoDB"
ALLOWED_HOSTS="URL del servidor"
DJANGO_API_URL="UrL del servidor"
YTDLP_COOKIES="Cookies de YTDLP"
```

### 3. Ejecutar el backend

```bash
python manage.py runserver 10000
```

### 4. Ejecutar el frontend

```bash
streamlit run streamlit_app/app.py
```

#  Autores

- Ricardo Esteban D’Alessandro Marroquín González
- Ricardo Adrián Colindres Franco 
- Oscar José Barrios Cotom
- Sara Rebeca Archila de León
- Axel David Hurtarte Mayen

---
