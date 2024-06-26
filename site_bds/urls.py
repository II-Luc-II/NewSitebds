from django.urls import path
from site_bds import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-message', views.contact_message, name='contact_message'),
    path('add-news-letter', views.add_news_letter, name='add-news-letter'),
    path('client-message', views.client_message_contact, name='client-message-contact'),
    path('add-news-letter-message', views.contact_message_newsletter, name='contact_message_newsletter'),
    path('page-success-client', views.page_success_client, name='page-success-client'),
    path('privacy', views.privacy, name='privacy'),
]

handler404 = views.handle404
