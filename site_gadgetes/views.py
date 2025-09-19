from django.shortcuts import render



def snack_game(request):
    return render(request, 'gadgets/snack-game.html')


