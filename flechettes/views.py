from django.shortcuts import render, redirect
from flechettes.models import Game


def index(request):
    games = Game.objects.all()

    context = {
        "games": games,
    }
    return render(request, 'index.html', context)


def game_selected_501(request):
    return render(request, 'site/game-selected_501.html')


def game_selected_301(request):
    return render(request, 'site/game-selected_301.html')


def game_description(request, game_id):
    game = Game.objects.get(id=game_id)

    context = {
        "game": game,
    }
    return render(request, 'site/game-description.html', context)