from django.urls import path

from . import views

app_name = 'customer'


urlpatterns = [
    # Ajout et modif client
    path('add-profil-customer', views.add_profil_customer, name='add_profil_customer'),
    path('edit-profil-customer/<int:customer_id>/', views.edit_profil_customer, name='edit_profil_customer'),   # Ajout et modif client pro
]