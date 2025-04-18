# videos/api.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from procesador import procesar_video, responder_pregunta
from conexion_mongo import coleccion, db  # ✅ Importamos la colección y la base de datos

from bson import ObjectId
import re

@api_view(['GET'])
def descargar_pdf(request):
    video_id = request.GET.get('id')
    if not video_id:
        return Response({'error': 'ID no proporcionado'}, status=400)

    if not re.fullmatch(r'[a-fA-F0-9]{24}', video_id):
        return Response({'error': 'ID con formato inválido'}, status=400)

    try:
        documento = coleccion.find_one({'_id': ObjectId(video_id)})
    except Exception:
        return Response({'error': 'ID inválido'}, status=400)

    if not documento:
        return Response({'error': 'Documento no encontrado'}, status=404)

    pdf_bytes = documento.get('pdf')
    if not pdf_bytes:
        return Response({'error': 'PDF no encontrado'}, status=404)

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{documento["titulo"]}.pdf"'
    return response

@api_view(['POST'])
def procesar(request):
    link = request.data.get('link')
    if not link:
        return Response({'error': 'Falta el link'}, status=400)
    
    resultado = procesar_video(link)

    if 'id' not in resultado:
        return Response({'error': 'ID no encontrado en el procesamiento'}, status=400)
    
    return Response({
        "transcripcion": resultado['transcripcion'],
        "titulo": resultado['titulo'],
        "id": resultado['id']
    })

@api_view(['POST'])
def preguntar(request):
    pregunta = request.data.get('pregunta')
    contenido = request.data.get('contenido')

    if not pregunta or not contenido:
        return Response({'error': 'Faltan pregunta o contenido'}, status=400)

    respuesta = responder_pregunta(pregunta, contenido)
    return Response({'respuesta': respuesta})

@api_view(['GET'])
def listar_videos(request):
    videos = coleccion.find({}, {"_id": 1, "titulo": 1, "url": 1})
    resultado = []

    for video in videos:
        resultado.append({
            "id": str(video["_id"]),
            "titulo": video.get("titulo", "Sin título"),
            "url": video.get("url", "Sin URL")
        })

    return Response(resultado)
