from django.urls import path
from site_gadgetes import views

urlpatterns = [
    path('video-youtube', views.video_youtube, name='video_youtube'),
    path('snack-game', views.snack_game, name='snack_game'),
]