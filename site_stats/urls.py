from django.urls import path
from . import views

urlpatterns = [
    path('site-list', views.site_list, name='site_list'),
]