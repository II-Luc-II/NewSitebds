from django.urls import path, include

from account import views


urlpatterns = [
    path('login', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='logout'),
]
