from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from site_bds.views import is_superuser


@user_passes_test(is_superuser)
def snack_game(request):
    return render(request, 'gadgets/snack-game.html')


