from django.db import models  # Importa el módulo models de Django para definir modelos.

class Video(models.Model):
    """
    Modelo que representa un video procesado.

    Campos:
        - titulo: Título del video.
        - link: Enlace al video (URL).
        - transcripcion: Texto de la transcripción del video.
        - pdf: Archivo PDF generado con la transcripción.
    """
    titulo = models.CharField(max_length=255)  # Campo de texto con un límite máximo de 255 caracteres.
    link = models.URLField()  # Campo para almacenar una URL válida.
    transcripcion = models.TextField()  # Campo de texto largo para la transcripción.
    pdf = models.FileField(upload_to="pdfs/", null=True, blank=True)  # Campo para almacenar el archivo PDF, opcional.

    def __str__(self):
        """
        Representación en cadena del modelo.

        Returns:
            str: El título del video.
        """
        return self.titulo