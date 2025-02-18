from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from BDS_Site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('site_bds.urls')),
    path('', include('account.urls')),
    path('', include('yourproject.urls')),
    path('', include('site_stats.urls')),
    path('', include('site_gadgetes.urls')),
    path('captcha/', include('captcha.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
