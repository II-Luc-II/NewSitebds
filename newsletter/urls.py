from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [

    path(
        "inscription/",
        views.subscribe,
        name="subscribe",
    ),

    path(
        "confirmation/<uuid:token>/",
        views.confirm_subscription,
        name="confirm",
    ),

    path(
        "desinscription/<uuid:token>/",
        views.unsubscribe,
        name="unsubscribe",
    ),

]
