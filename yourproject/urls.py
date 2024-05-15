from django.urls import path
from yourproject import views

urlpatterns = [
    path('your-project', views.your_project, name='your-project'),
    path('devis-message', views.devis_message, name='devis-message'),
    path('page-success', views.page_success, name='page-success'),
    path('client-message', views.client_message, name='client-message'),
]