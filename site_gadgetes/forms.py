# forms.py
from django import forms


class YouTubeDownloadForm(forms.Form):
    video_url = forms.URLField(label='Lien de la vidéo YouTube',
                               max_length=200,
                               widget=forms.URLInput(attrs={'class': 'form-control'}))
