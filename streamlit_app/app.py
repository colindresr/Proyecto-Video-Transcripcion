# app.py
import os
import streamlit as st
import requests

DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://localhost:10000")

# ===== Cargar estilos =====
def cargar_css(ruta):
    with open(ruta) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = os.path.join(os.path.dirname(__file__), "styles.css")
cargar_css(css_path)

# ===== Navbar =====
st.sidebar.markdown('<h2 class="stTitle">📚 Navegación</h2>', unsafe_allow_html=True)
pagina = st.sidebar.radio("Ir a:", ["Inicio", "Chat"])

# ===== Inicio =====
if pagina == "Inicio":
    st.markdown('<h1 class="titulo-app">Bienvenido al Asistente de Video</h1>', unsafe_allow_html=True)
    st.markdown('<div class="texto-grande">Utiliza el menú lateral para comenzar a transcribir y hacer preguntas sobre videos.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="texto-grande">
        Este proyecto es una herramienta interactiva que te permite transcribir videos de plataformas como YouTube
        e interactuar con su contenido mediante preguntas en lenguaje natural.
        <br><br>
        🔍 <strong>¿Qué puedes hacer con esta app?</strong>
        <ul>
            <li>📹 Ingresar el enlace de un video y obtener su transcripción completa.</li>
            <li>📁 Subir un archivo .txt con múltiples enlaces y procesarlos en lote.</li>
            <li>📄 Descargar la transcripción en formato PDF.</li>
            <li>💬 Hacer preguntas sobre el contenido del video y obtener respuestas inteligentes.</li>
        </ul>
        <br>
        Utiliza el menú lateral para comenzar. ¡Explora y saca el máximo provecho a tus videos!
        <br><br>
        🔧  <strong>Tecnologías utilizadas en este proyecto:</strong>
        <ul>
            <li><strong>Streamlit</strong> para la interfaz web interactiva.</li>
            <li><strong>Django</strong> con Django REST Framework para el backend y API.</li>
            <li><strong>Python</strong> como lenguaje de programación principal.</li>
            <li><strong>ffmpeg</strong> para procesar videos y extraer audio.</li>
            <li><strong>MongoDB</strong> para almacenar transcripciones y otros datos.</li>
            <li><strong>Requests</strong> para la interacción con la API.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>Importante:</strong> Esta aplicación utiliza una <strong>API interna</strong> para procesar y transcribir videos, así como para responder preguntas mediante inteligencia artificial.
        <br><br>
        📡 Las peticiones realizadas desde esta interfaz se comunican con un servidor backend local o desplegado, el cual se encarga del procesamiento del audio, la transcripción, la generación del PDF y la interacción con modelos de lenguaje.
        <br><br>
        🛡️ <strong>Privacidad:</strong> No se almacena información sensible del usuario. Las transcripciones y PDFs generados se guardan únicamente con fines de visualización y consulta dentro de la sesión.
        <br><br>
        🧪 Esta herramienta es experimental y se encuentra en desarrollo. Puede haber errores o limitaciones en los resultados.
    </div>
    """, unsafe_allow_html=True)

# ===== Chat =====
elif pagina == "Chat":
    st.markdown('<h1 class="titulo-app">Asistente de Video</h1>', unsafe_allow_html=True)
    st.markdown('<div class="header-custom">🔗 Ingresar link directamente</div>', unsafe_allow_html=True)
    link = st.text_input("Pega el link del video aquí")

    if st.button("Transcribir video"):
        if link:
            with st.spinner("Procesando video..."):
                res = requests.post(f"{DJANGO_API_URL}/api/procesar/", json={"link": link})

                if res.status_code == 200:
                    try:
                        data = res.json()
                        if "transcripcion" in data and "titulo" in data and "id" in data:
                            st.session_state["transcripcion"] = data["transcripcion"]
                            st.session_state["titulo"] = data["titulo"]
                            st.session_state["id"] = data["id"]
                            st.success(f"✅ {data['titulo']} transcrito con éxito")

                            pdf_id = data.get("id")
                            st.markdown(
                                f'<div class="link-limpio"><a href="{DJANGO_API_URL}/api/descargar_pdf/?id={pdf_id}" target="_blank">📥 Descargar PDF desde servidor</a></div>',
                                unsafe_allow_html=True
                            )
                        else:
                            st.error("❌ La respuesta no contiene la transcripción esperada.")
                            st.json(data)
                    except Exception as e:
                        st.error(f"❌ Error interpretando la respuesta del servidor: {e}")
                        st.write(res.text)
                else:
                    st.error(f"❌ Error procesando el video. Código: {res.status_code}")
                    try:
                        st.json(res.json())
                    except:
                        st.write(res.text)

    st.divider()
    st.markdown('<div class="header-custom">📄 Subir archivo .txt con links</div>', unsafe_allow_html=True)
    archivo = st.file_uploader("Selecciona un archivo .txt", type=["txt"])

    if archivo is not None:
        contenido = archivo.read().decode("utf-8")
        links = [line.strip() for line in contenido.splitlines() if line.strip()]
        if st.button("Procesar archivo"):
            resultados = []
            for i, url in enumerate(links):
                with st.spinner(f"Procesando {url}..."):
                    res = requests.post(f"{DJANGO_API_URL}/api/procesar/", json={"link": url})
                    if res.status_code == 200:
                        try:
                            data = res.json()
                            resultados.append(data)
                            st.success(f"{i+1}. ✅ {data.get('titulo', 'Sin título')}")
                        except:
                            st.error(f"{i+1}. ❌ Error al interpretar respuesta para: {url}")
                    else:
                        st.error(f"{i+1}. ❌ Error al procesar: {url}")
            st.session_state["batch_resultados"] = resultados

    st.divider()
    if "transcripcion" in st.session_state:
        st.markdown('<div class="subheader-custom">📝 Transcripción:</div>', unsafe_allow_html=True)
        st.text_area("Texto", value=st.session_state["transcripcion"], height=300)

        pregunta = st.text_input("❓ Haz una pregunta sobre el video")
        if st.button("Preguntar") and pregunta:
            with st.spinner("Buscando respuesta..."):
                res = requests.post(f"{DJANGO_API_URL}/api/preguntar/", json={
                    "pregunta": pregunta,
                    "contenido": st.session_state["transcripcion"]
                })
                if res.status_code == 200:
                    respuesta = res.json().get("respuesta", "Sin respuesta")
                    st.markdown('<div class="subheader-custom">💬 Respuesta:</div>', unsafe_allow_html=True)
                    st.write(respuesta)
                else:
                    st.error("❌ Error al enviar la pregunta")

    if "batch_resultados" in st.session_state:
        st.markdown('<div class="subheader-custom">📦 Resultados del archivo:</div>', unsafe_allow_html=True)
        for item in st.session_state["batch_resultados"]:
            st.markdown(f"<div class='texto-grande'><strong>{item.get('titulo', 'Sin título')}</strong></div>", unsafe_allow_html=True)
            st.text_area("Transcripción", value=item.get("transcripcion", ""), height=200, key=f"transcripcion_{item.get('id', '')}")
            if 'id' in item:
                st.markdown(
                    f'<div class="link-limpio"><a href="{DJANGO_API_URL}/api/descargar_pdf/?id={item["id"]}" target="_blank">📥 Descargar PDF desde servidor</a></div>',
                    unsafe_allow_html=True
                )
            with st.form(key=f"form_{item.get('id', i)}"):
                pregunta = st.text_input("❓ Haz una pregunta sobre este video", key=f"pregunta_{item.get('id', i)}")
                submit = st.form_submit_button("Preguntar")
                if submit and pregunta:
                    with st.spinner("Buscando respuesta..."):
                        res = requests.post(f"{DJANGO_API_URL}/api/preguntar/", json={
                            "pregunta": pregunta,
                            "contenido": item.get("transcripcion", "")
                        })
                        if res.status_code == 200:
                            respuesta = res.json().get("respuesta", "Sin respuesta")
                            st.markdown("💬 **Respuesta:**")
                            st.write(respuesta)
                        else:
                            st.error("❌ Error al enviar la pregunta")
