import os
from celery import Celery
from django.conf import settings

# Définir le module de paramètres Django par défaut
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDS_Site.settings')

# Créer une instance de Celery
app = Celery('BDS_Site')

# Charger la configuration depuis le fichier de paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks dans toutes les apps déclarées dans INSTALLED_APPS
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

