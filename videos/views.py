from django.shortcuts import render, redirect
from .forms import LinkForm, PreguntaForm
from .models import Video
from procesador import procesar_video, responder_pregunta
from django.core.files.base import ContentFile
from django.views.generic import TemplateView

class FrontendAppView(TemplateView):
    template_name = "index.html"


def home(request):
    form = LinkForm()
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            resultado = procesar_video(link)

            # Crear y guardar el objeto Video
            video = Video(
                titulo=resultado['titulo'],
                link=link,
                transcripcion=resultado['transcripcion']
            )

            # Cargar el contenido del PDF desde la ruta generada
            with open(resultado['pdf_path'], 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                video.pdf.save(f"{video.titulo}.pdf", ContentFile(pdf_content))

            video.save()
            return redirect('resultado', video_id=video.id)

    return render(request, 'videos/home.html', {'form': form})

def resultado(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'videos/resultado.html', {'video': video})

def pregunta(request, video_id):
    video = Video.objects.get(id=video_id)
    form = PreguntaForm()
    respuesta = None

    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']
            respuesta = responder_pregunta(pregunta, {
                'transcripcion': video.transcripcion
            })

    return render(request, 'videos/pregunta.html', {'video': video, 'form': form, 'respuesta': respuesta})
