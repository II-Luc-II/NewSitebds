from allauth.account.models import EmailAddress
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging



logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_mail_batch(self, subject, html_message, plain_message, recipient_batch, from_email, reply_to=None, headers=None):
    """
    Envoie un e-mail HTML+texte à un lot de destinataires.
    - subject: str
    - html_message: str (peut être None)
    - plain_message: str (fallback si html absent ; si None, on dérive de html)
    - recipient_batch: list[str]
    - from_email: str
    - reply_to: list[str] | None
    - headers: dict | None
    Retourne le nombre de destinataires acceptés par le backend.
    """
    try:
        if not recipient_batch:
            logger.warning("send_mail_batch appelé sans destinataires.")
            return 0

        if not plain_message:
            plain_message = strip_tags(html_message or "")

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_batch,
            reply_to=reply_to or None,
            headers=headers or None,
        )

        if html_message:
            email.attach_alternative(html_message, "text/html")

        sent = email.send()
        logger.info("Email '%s' envoyé à %d destinataire(s).", subject, sent)
        return sent
    except Exception as e:
        # Celery va auto-retry grâce à autoretry_for + retry_backoff
        logger.exception("Échec envoi email '%s' (tentative %s): %s", subject, getattr(self.request, 'retries', 0), e)
        raise


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def cleanup_unconfirmed_allauth_accounts(self, days=None):
    """
    Supprime les adresses e-mail allauth non confirmées trop anciennes.
    Supprime aussi les utilisateurs qui n'ont plus aucune adresse e-mail confirmée.

    Par défaut, utilise ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS, sinon 3 jours.
    """

    expire_days = days or getattr(settings, "ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", 3)
    cutoff = timezone.now() - timedelta(days=expire_days)

    User = get_user_model()

    # Utilisateurs ayant une adresse non vérifiée ancienne
    unverified_emails = EmailAddress.objects.filter(
        verified=False,
        user__date_joined__lt=cutoff,
    ).select_related("user")

    user_ids = list(
        unverified_emails.values_list("user_id", flat=True).distinct()
    )

    deleted_email_count, _ = unverified_emails.delete()

    deleted_user_count = 0

    for user in User.objects.filter(id__in=user_ids):
        has_verified_email = EmailAddress.objects.filter(
            user=user,
            verified=True,
        ).exists()

        if not has_verified_email:
            user.delete()
            deleted_user_count += 1

    logger.info(
        "Nettoyage allauth terminé: %s adresse(s) non confirmée(s), %s utilisateur(s) supprimé(s).",
        deleted_email_count,
        deleted_user_count,
    )

    return {
        "deleted_unverified_emails": deleted_email_count,
        "deleted_users": deleted_user_count,
        "expire_days": expire_days,
    }