from django.shortcuts import render, redirect  # Importa funciones para renderizar plantillas y redirigir solicitudes.
from .forms import LinkForm, PreguntaForm  # Importa los formularios definidos en forms.py.
from .models import Video  # Importa el modelo Video para interactuar con la base de datos.
from procesador import procesar_video, responder_pregunta  # Importa funciones para procesar videos y responder preguntas.
from django.core.files.base import ContentFile  # Importa ContentFile para manejar archivos en memoria.
from django.views.generic import TemplateView  # Importa TemplateView para vistas basadas en clases.

class FrontendAppView(TemplateView):
    """
    Vista genérica para servir la plantilla principal del frontend.
    """
    template_name = "index.html"  # Especifica la plantilla que se renderizará.

def home(request):
    """
    Vista para la página principal donde se ingresa el enlace del video.

    Args:
        request: Solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla 'videos/home.html' con el formulario.
    """
    form = LinkForm()  # Inicializa el formulario para ingresar el enlace.
    if request.method == 'POST':
        form = LinkForm(request.POST)  # Procesa los datos enviados en el formulario.
        if form.is_valid():
            link = form.cleaned_data['link']  # Obtiene el enlace validado.
            resultado = procesar_video(link)  # Procesa el video usando la función `procesar_video`.

            # Crear y guardar el objeto Video en la base de datos.
            video = Video(
                titulo=resultado['titulo'],
                link=link,
                transcripcion=resultado['transcripcion']
            )

            # Cargar el contenido del PDF desde la ruta generada.
            with open(resultado['pdf_path'], 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                video.pdf.save(f"{video.titulo}.pdf", ContentFile(pdf_content))  # Guarda el PDF en el modelo.

            video.save()  # Guarda el objeto Video en la base de datos.
            return redirect('resultado', video_id=video.id)  # Redirige a la vista de resultados.

    return render(request, 'videos/home.html', {'form': form})  # Renderiza la plantilla con el formulario.

def resultado(request, video_id):
    """
    Vista para mostrar los resultados del procesamiento de un video.

    Args:
        request: Solicitud HTTP.
        video_id: ID del video procesado.

    Returns:
        HttpResponse: Renderiza la plantilla 'videos/resultado.html' con los datos del video.
    """
    video = Video.objects.get(id=video_id)  # Obtiene el video de la base de datos.
    return render(request, 'videos/resultado.html', {'video': video})  # Renderiza la plantilla con el video.

def pregunta(request, video_id):
    """
    Vista para realizar preguntas sobre la transcripción de un video.

    Args:
        request: Solicitud HTTP.
        video_id: ID del video sobre el cual se hará la pregunta.

    Returns:
        HttpResponse: Renderiza la plantilla 'videos/pregunta.html' con la respuesta generada.
    """
    video = Video.objects.get(id=video_id)  # Obtiene el video de la base de datos.
    form = PreguntaForm()  # Inicializa el formulario para ingresar la pregunta.
    respuesta = None  # Variable para almacenar la respuesta generada.

    if request.method == 'POST':
        form = PreguntaForm(request.POST)  # Procesa los datos enviados en el formulario.
        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']  # Obtiene la pregunta validada.
            respuesta = responder_pregunta(pregunta, {  # Genera la respuesta usando la función `responder_pregunta`.
                'transcripcion': video.transcripcion
            })

    return render(request, 'videos/pregunta.html', {'video': video, 'form': form, 'respuesta': respuesta})  # Renderiza la plantilla con la respuesta.