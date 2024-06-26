from django.urls import path
from site_gadgetes import views

urlpatterns = [
    path('video-youtube', views.video_youtube, name='video_youtube'),
]