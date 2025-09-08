from django.shortcuts import render
from django.contrib import messages
from pytube import YouTube
from django.http import StreamingHttpResponse
import requests
import time
from pytube.exceptions import PytubeError
import logging



def snack_game(request):
    return render(request, 'gadgets/snack-game.html')


