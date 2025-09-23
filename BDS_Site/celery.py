import os
from celery import Celery

# Définir le module de paramètres Django par défaut
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDS_Site.settings')

# Créer une instance de Celery
app = Celery('BDS_Site')

# Charger la configuration depuis le fichier de paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered Django app configs
app.autodiscover_tasks()

# Configurer le broker Redis
app.conf.update(
    broker_url='redis://127.0.0.1:6379/0',
    result_backend='redis://127.0.0.1:6379/0',
)
