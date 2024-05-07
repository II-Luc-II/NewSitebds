from django.urls import path
from site_bds import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-message', views.contact_message, name='contact_message'),
]