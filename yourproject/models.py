from django.db import models


class Question(models.Model):
    questions_1 = models.CharField(max_length=255)
    questions_2 = models.CharField(max_length=255)
    questions_3 = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    entreprise =models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = 'Devis'
        verbose_name = 'Devis'









