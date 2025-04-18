from django import forms

class LinkForm(forms.Form):
    link = forms.URLField(label="Link de YouTube", widget=forms.URLInput(attrs={'class': 'form-control'}))

class PreguntaForm(forms.Form):
    pregunta = forms.CharField(label="Pregunta", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
