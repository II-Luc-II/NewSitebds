from django.urls import path
from site_gadgetes import views

urlpatterns = [
    path('snack-game', views.snack_game, name='snack_game'),
]