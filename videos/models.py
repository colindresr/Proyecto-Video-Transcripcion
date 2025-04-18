from django.db import models

class Video(models.Model):
    titulo = models.CharField(max_length=255)
    link = models.URLField()
    transcripcion = models.TextField()
    pdf = models.FileField(upload_to="pdfs/", null=True, blank=True)

    def __str__(self):
        return self.titulo