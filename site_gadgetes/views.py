from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from pytube import YouTube
import os
from django.conf import settings
from .forms import YouTubeDownloadForm


from django.http import StreamingHttpResponse
import requests

def video_youtube(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()

                def generate():
                    for chunk in requests.get(stream.url, stream=True).iter_content(chunk_size=8192):
                        yield chunk

                response = StreamingHttpResponse(generate(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'

                messages.success(request, 'La vidéo est bien téléchargée.')
                return response

            except Exception as e:
                messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')

    else:
        form = YouTubeDownloadForm()

    return render(request, 'gadgets/video-youtube.html', {'form': form})

