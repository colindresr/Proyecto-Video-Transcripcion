# videos/api.py

from rest_framework.decorators import api_view  # Decorador para definir vistas basadas en funciones.
from rest_framework.response import Response  # Clase para devolver respuestas HTTP en formato JSON.
from django.http import HttpResponse  # Clase para devolver respuestas HTTP estándar.
from procesador import procesar_video, responder_pregunta  # Funciones para procesar videos y responder preguntas.
from conexion_mongo import coleccion, db  # Importa la colección y la base de datos de MongoDB.

from bson import ObjectId  # Clase para manejar IDs de documentos en MongoDB.
import re  # Módulo para trabajar con expresiones regulares.

@api_view(['GET'])
def descargar_pdf(request):
    """
    Descarga el PDF asociado a un video desde MongoDB.

    Args:
        request: Solicitud HTTP con el parámetro 'id' del video.

    Returns:
        HttpResponse: Respuesta con el archivo PDF o un mensaje de error.
    """
    video_id = request.GET.get('id')  # Obtiene el ID del video desde los parámetros de la solicitud.
    if not video_id:
        return Response({'error': 'ID no proporcionado'}, status=400)

    # Verifica que el ID tenga el formato correcto (24 caracteres hexadecimales).
    if not re.fullmatch(r'[a-fA-F0-9]{24}', video_id):
        return Response({'error': 'ID con formato inválido'}, status=400)

    try:
        # Busca el documento en la colección de MongoDB.
        documento = coleccion.find_one({'_id': ObjectId(video_id)})
    except Exception:
        return Response({'error': 'ID inválido'}, status=400)

    if not documento:
        return Response({'error': 'Documento no encontrado'}, status=404)

    pdf_bytes = documento.get('pdf')  # Obtiene los datos del PDF del documento.
    if not pdf_bytes:
        return Response({'error': 'PDF no encontrado'}, status=404)

    # Devuelve el PDF como una respuesta HTTP con el archivo adjunto.
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{documento["titulo"]}.pdf"'
    return response

@api_view(['POST'])
def procesar(request):
    """
    Procesa un video desde una URL, lo transcribe y guarda los datos en MongoDB.

    Args:
        request: Solicitud HTTP con el enlace del video en el cuerpo.

    Returns:
        Response: Respuesta con los datos procesados o un mensaje de error.
    """
    link = request.data.get('link')  # Obtiene el enlace del video desde el cuerpo de la solicitud.
    if not link:
        return Response({'error': 'Falta el enlace del video.'}, status=400)

    resultado = procesar_video(link)  # Procesa el video usando la función `procesar_video`.

    if resultado is None:
        return Response({'error': 'No se pudo procesar el video. Revisa si requiere autenticación o cookies.'}, status=500)

    return Response(resultado)  # Devuelve el resultado del procesamiento.

@api_view(['POST'])
def preguntar(request):
    """
    Responde una pregunta basada en la transcripción de un video.

    Args:
        request: Solicitud HTTP con la pregunta y el contenido en el cuerpo.

    Returns:
        Response: Respuesta con la respuesta generada o un mensaje de error.
    """
    pregunta = request.data.get('pregunta')  # Obtiene la pregunta desde el cuerpo de la solicitud.
    contenido = request.data.get('contenido')  # Obtiene el contenido (transcripción) desde el cuerpo.

    if not pregunta or not contenido:
        return Response({'error': 'Faltan pregunta o contenido'}, status=400)

    respuesta = responder_pregunta(pregunta, contenido)  # Genera la respuesta usando la función `responder_pregunta`.
    return Response({'respuesta': respuesta})  # Devuelve la respuesta generada.

@api_view(['GET'])
def listar_videos(request):
    """
    Lista todos los videos almacenados en MongoDB.

    Args:
        request: Solicitud HTTP.

    Returns:
        Response: Respuesta con una lista de videos (ID, título y URL).
    """
    videos = coleccion.find({}, {"_id": 1, "titulo": 1, "url": 1})  # Obtiene los videos de la colección.
    resultado = []

    # Recorre los videos y los agrega a la lista de resultados.
    for video in videos:
        resultado.append({
            "id": str(video["_id"]),  # Convierte el ID de MongoDB a una cadena.
            "titulo": video.get("titulo", "Sin título"),  # Obtiene el título o un valor predeterminado.
            "url": video.get("url", "Sin URL")  # Obtiene la URL o un valor predeterminado.
        })

    return Response(resultado)  # Devuelve la lista de videos.