from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nom")
    players_nbr_min = models.IntegerField(default=1, verbose_name="Nbr de joueurs minimum")
    players_nbr_max= models.IntegerField(default=1, verbose_name="Nbr de joueurs maximum")
    level = models.CharField(max_length=60, blank=True, null=True, verbose_name="Difficulté")
    objectif = models.CharField(max_length=300, blank=True, null=True, verbose_name="Objectif")
    game_time = models.IntegerField(default=10, verbose_name="Temps de partie")
    description = models.TextField(verbose_name="Description")
    url = models.URLField(blank=True, null=True, verbose_name="URL du jeu")
    in_line = models.BooleanField(default=False, verbose_name="En ligne")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "Les jeux de flechettes"
        verbose_name_plural = "Les jeux de flechettes"
        ordering = ('name',)

    def __str__(self):
        return self.name