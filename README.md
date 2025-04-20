# 📹 Asistente de Transcripción de Videos

Este proyecto es una aplicación web que permite transcribir videos de YouTube, guardar la transcripción en PDF y hacer preguntas sobre el contenido del video. Está desarrollado con **Streamlit** como frontend, **Django REST Framework** como backend, y usa **MongoDB** para almacenar los datos.

---

## 🚀 Funcionalidades

- 📥 Subida de links de videos de YouTube o archivos `.txt` con múltiples enlaces.
- 🧠 Transcripción automática de audio (con Whisper).
- 📄 Generación y almacenamiento de transcripción en formato PDF.
- 🤖 Preguntas y respuestas sobre el contenido del video (usando un modelo LLM).
- 💾 Almacenamiento de PDFs y transcripciones en MongoDB.
- 🧭 Navegación sencilla entre secciones (`Inicio` y `Chat`) desde el frontend.

---

## 🧰 Tecnologías Usadas

### Backend
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytube](https://pytube.io/) / `yt-dlp` para descarga de videos
- [OpenAI Whisper](https://github.com/openai/whisper) para transcripción
- [PyMuPDF](https://pymupdf.readthedocs.io/) para generación de PDFs
- [pymongo](https://pymongo.readthedocs.io/) para conexión a MongoDB

### Frontend
- [Streamlit](https://streamlit.io/)
- Estilizado con `styles.css`
- Navegación por secciones y subida de archivos

### Base de Datos
- [MongoDB Atlas](https://www.mongodb.com/atlas) para almacenamiento en la nube

---

## ⚙️ Configuración Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/colindresr/Proyecto-Video-Transcripcion.git
cd proyecto-video-transcripcion
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

