from django.urls import path
from . import views

urlpatterns = [
    path('stats', views.visitor_statistics, name='visitor_statistics'),
    path('site-list', views.site_list, name='site_list'),
]