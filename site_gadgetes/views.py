from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from pytube import YouTube
import os
from django.conf import settings
from .forms import YouTubeDownloadForm


def video_youtube(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()
                video_title = yt.title

                # Assurez-vous que le répertoire 'media/downloads' existe
                download_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

                download_path = os.path.join(download_dir, f'{video_title}.mp4')
                stream.download(output_path=download_dir, filename=f'{video_title}.mp4')

                # Indiquer que le téléchargement est en cours
                messages.info(request, 'Téléchargement en cours...')

                # Renvoyer la vidéo en tant que téléchargement direct
                file_path = os.path.join(download_dir, f'{video_title}.mp4')
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        response = HttpResponse(f.read(), content_type='application/force-download')
                        response['Content-Disposition'] = f'attachment; filename="{video_title}.mp4"'

                        # Supprimer le fichier après le téléchargement
                        os.remove(file_path)

                        # Définir la variable de session pour indiquer que le téléchargement est réussi
                        request.session['download_success'] = True

                        return response
                else:
                    messages.error(request, 'Fichier de vidéo introuvable après téléchargement.')

            except Exception as e:
                # Gestion des erreurs lors du téléchargement
                messages.error(request, f'Erreur lors du téléchargement de la vidéo : {str(e)}')
                # Réinitialiser l'indicateur de session pour l'échec
                request.session['download_success'] = False

    else:
        form = YouTubeDownloadForm()

    # Vérifier la session pour le message de fin de téléchargement
    if request.session.get('download_success'):
        messages.success(request, 'La vidéo est bien téléchargée.')
        # Réinitialiser l'indicateur de session après l'affichage du message
        del request.session['download_success']

    return render(request, 'gadgets/video-youtube.html', {'form': form})

