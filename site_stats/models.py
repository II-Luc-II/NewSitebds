from django.db import models


class Visitor(models.Model):
    visitor_id = models.CharField(max_length=32, unique=True, verbose_name="Visiteur ID")
    date_visited = models.DateTimeField(auto_now_add=True, verbose_name="Date de la visite")


class Site(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du site")
    url = models.URLField(verbose_name="URL du site")
    status = models.BooleanField(default=True, verbose_name="Statut (en ligne/hors ligne)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return self.name

class Vpn(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'app")
    host = models.CharField(max_length=100, verbose_name="Nom du vpn")
    url = models.URLField(verbose_name="URL du site")
    status = models.BooleanField(default=True, verbose_name="Statut (en ligne/hors ligne)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return self.name