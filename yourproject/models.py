from django.db import models


class Question(models.Model):
    questions_1 = models.CharField(max_length=255, verbose_name='Besoin')
    questions_2 = models.CharField(max_length=255, verbose_name='Budget')
    questions_3 = models.CharField(max_length=255, verbose_name='Démarrage')
    description = models.TextField()
    author = models.CharField(max_length=255, verbose_name='Auteur')
    entreprise =models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=255)
    checked = models.BooleanField(default=False, verbose_name='Traité')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Création Date')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = 'Devis Clients'
        verbose_name = 'Devis Client'









