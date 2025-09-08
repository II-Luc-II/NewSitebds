from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")

    phone_validator = RegexValidator(
        regex=r'^(?:\+33|0)[1-9](?:\d{8})$',
        message="Entrez un numéro de téléphone valide (ex: +33612345678 ou 0612345678)."
    )

    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        verbose_name="Numéro de téléphone"
    )
    email = models.EmailField()
    address = models.CharField(max_length=50, verbose_name="Adresse")
    entreprise = models.CharField(max_length=50, null=True, blank=True, verbose_name="Entreprise")
    mail = models.EmailField(verbose_name="Mail")
    complement_address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Complément d'adresse")
    city = models.CharField(max_length=50, verbose_name="Ville")
    created_at = models.DateTimeField(auto_now_add=True)
    zip_code = models.CharField(
        verbose_name="Code Postal",
        max_length=5,
        validators=[RegexValidator(r'^\d{5}$', "Entrez un code postal valide (5 chiffres).")]
    )
    image = models.ImageField(upload_to='photos-customer', null=True, blank=True)
    register_web = models.BooleanField(default=False, verbose_name="Inscription web")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



