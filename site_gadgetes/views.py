from django.shortcuts import render
from django.contrib import messages
from pytube import YouTube
from .forms import YouTubeDownloadForm
from django.http import StreamingHttpResponse
import requests
import time
from pytube.exceptions import PytubeError
import logging

# Configurer le logger
logging.basicConfig(level=logging.CRITICAL,
                    filename='gadgets.log',
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.debug("La fonction a bien été exécutée")
logging.info("Message d'information général")
logging.warning("Une erreur est arrivée")
logging.critical("Erreur critique")


def video_youtube(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            attempts = 0
            max_attempts = 5  # Limite de tentatives
            delay = 5  # Initial delay between retries

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
                    logging.info(f'Vidéo téléchargée : {yt.title}')
                    return response

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        attempts += 1
                        messages.info(request, f'Trop de requêtes. Réessai dans {delay} secondes... (Tentative {attempts} de {max_attempts})')
                        logging.warning(f'Trop de requêtes (Tentative {attempts}). Attente de {delay} secondes.')
                        time.sleep(delay)  # Attente de `delay` secondes avant de réessayer
                        delay *= 2  # Exponential backoff
                    else:
                        messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')
                        logging.error(f'Erreur HTTP {e.response.status_code} lors du téléchargement : {str(e)}')
                        break  # Sortir de la boucle en cas d'autre erreur

                except PytubeError as e:
                    messages.error(request, f'Erreur Pytube : {str(e)}')
                    logging.error(f'Erreur Pytube : {str(e)}')
                    break  # Sortir de la boucle en cas d'erreur Pytube

                except Exception as e:
                    messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')
                    logging.error(f'Erreur inconnue lors du téléchargement : {str(e)}')
                    break  # Sortir de la boucle en cas d'autre erreur

            if attempts == max_attempts:
                messages.error(request, 'Impossible de télécharger la vidéo après plusieurs tentatives.'
                                        ' Veuillez réessayer plus tard.')
                logging.error('Échec du téléchargement après plusieurs tentatives.')

    else:
        form = YouTubeDownloadForm()

    return render(request, 'gadgets/video-youtube.html', {'form': form})


