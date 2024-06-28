from django.shortcuts import render
from django.contrib import messages
from pytube import YouTube
from .forms import YouTubeDownloadForm
from django.http import StreamingHttpResponse
import requests
import time
from pytube.exceptions import PytubeError


def video_youtube(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            attempts = 0
            max_attempts = 5  # Limite de tentatives

            while attempts < max_attempts:
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

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        attempts += 1
                        messages.info(request, f'Trop de requêtes. Réessai dans 5 secondes... (Tentative {attempts} de {max_attempts})')
                        time.sleep(5)  # Attente de 5 secondes avant de réessayer
                    else:
                        messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')
                        break  # Sortir de la boucle en cas d'autre erreur

                except PytubeError as e:
                    messages.error(request, f'Erreur Pytube : {str(e)}')
                    break  # Sortir de la boucle en cas d'erreur Pytube

                except Exception as e:
                    messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')
                    break  # Sortir de la boucle en cas d'autre erreur

            if attempts == max_attempts:
                messages.error(request, 'Impossible de télécharger la vidéo après plusieurs tentatives.'
                                        ' Veuillez réessayer plus tard.')

    else:
        form = YouTubeDownloadForm()

    return render(request, 'gadgets/video-youtube.html', {'form': form})


