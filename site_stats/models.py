from django.db import models


class Visitor(models.Model):
    visitor_id = models.CharField(max_length=32, unique=True, verbose_name="Visiteur ID")
    date_visited = models.DateTimeField(auto_now_add=True, verbose_name="Date de la visite")

