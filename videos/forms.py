from django import forms  # Importa el módulo forms de Django para crear formularios.

class LinkForm(forms.Form):
    """
    Formulario para ingresar un enlace de YouTube.

    Campos:
        - link: Campo de tipo URL para ingresar el enlace del video.
    """
    link = forms.URLField(
        label="Link de YouTube",  # Etiqueta del campo.
        widget=forms.URLInput(attrs={'class': 'form-control'})  # Personaliza el widget con clases CSS.
    )

class PreguntaForm(forms.Form):
    """
    Formulario para ingresar una pregunta sobre un video.

    Campos:
        - pregunta: Campo de texto para ingresar la pregunta.
    """
    pregunta = forms.CharField(
        label="Pregunta",  # Etiqueta del campo.
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})  # Personaliza el widget como un área de texto.
    )