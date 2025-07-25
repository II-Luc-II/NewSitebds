from django.urls import path
from site_bds import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from .views import robots_txt


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('contact-message', views.contact_message, name='contact_message'),
    path('contact', views.contact, name='contact'),
    # formulaire pop-up contact
    path('contact-form/', views.contact_form_view, name='contact_form_view'),
    path('add-news-letter', views.add_news_letter, name='add-news-letter'),
    path('client-message', views.client_message_contact, name='client-message-contact'),
    path('add-news-letter-message', views.contact_message_newsletter, name='contact_message_newsletter'),
    path('page-success-client', views.page_success_client, name='page-success-client'),
    path('privacy', views.privacy, name='privacy'),
    path('news', views.news, name='news'),
    path('blog-single/<int:blog_id>', views.blog_single, name='blog_single'),
    path('gallery-single/<int:gallery_id>', views.gallery_single, name='gallery_single'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', robots_txt),
]

handler404 = views.handle404
