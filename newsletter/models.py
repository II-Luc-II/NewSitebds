
from django_ckeditor_5.fields import CKEditor5Field

import uuid

from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):

    email = models.EmailField(
        unique=True,
        verbose_name="Adresse e-mail",
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="Abonnement actif",
    )

    is_confirmed = models.BooleanField(
        default=False,
        verbose_name="Adresse confirmée",
    )

    confirmation_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription",
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de confirmation",
    )

    unsubscribed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de désinscription",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"

    def __str__(self):
        return self.email

    def confirm(self):
        """
        Confirme l'inscription à la newsletter.
        """

        self.is_confirmed = True
        self.is_active = True
        self.confirmed_at = timezone.now()
        self.unsubscribed_at = None

        self.save(
            update_fields=[
                "is_confirmed",
                "is_active",
                "confirmed_at",
                "unsubscribed_at",
            ]
        )

    def unsubscribe(self):
        """
        Désabonne l'utilisateur de la newsletter.
        """

        self.is_active = False
        self.unsubscribed_at = timezone.now()

        self.save(
            update_fields=[
                "is_active",
                "unsubscribed_at",
            ]
        )


class Newsletter(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        QUEUED = "QUEUED", "En attente d'envoi"
        SENT = "SENT", "Envoyée"

    subject = models.CharField(
        max_length=255,
        verbose_name="Objet",
    )

    content = CKEditor5Field(
        "Contenu",
        config_name="default",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Statut",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification",
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"

    def __str__(self):
        return self.subject


class NewsletterDelivery(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        SENT = "SENT", "Envoyé"
        FAILED = "FAILED", "Échec"

    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    subscriber = models.ForeignKey(
        NewsletterSubscriber,
        on_delete=models.CASCADE,
        related_name="newsletter_deliveries",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "newsletter",
                    "subscriber",
                ],
                name="unique_newsletter_delivery",
            ),
        ]

    def __str__(self):
        return (
            f"{self.newsletter} - "
            f"{self.subscriber.email} - "
            f"{self.get_status_display()}"
        )