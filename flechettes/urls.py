from django.urls import path
from . import views

app_name = "flechettes"

urlpatterns = [

    # Gestion du bandeau
    path('', views.index, name='index'),

    # ---- Game -------
    path('game_selected_501', views.game_selected_501, name='game_selected_501'),
    path('game_selected_301', views.game_selected_301, name='game_selected_301'),
    # ---- Game description -------
    path('game_description/<int:game_id>', views.game_description, name='game_description'),
]
