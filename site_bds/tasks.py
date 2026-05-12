from allauth.account.models import EmailAddress
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging

from django.db.models import Q

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


@shared_task(bind=True)
def cleanup_unconfirmed_allauth_accounts(self):
    User = get_user_model()

    expire_days = getattr(settings, "ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS", 3)
    cutoff = timezone.now() - timedelta(days=expire_days)

    users_to_delete = User.objects.filter(
        date_joined__lt=cutoff
    ).filter(
        Q(emailaddress__verified=False) | Q(emailaddress__isnull=True)
    ).exclude(
        emailaddress__verified=True
    ).distinct()

    deleted_users_count = users_to_delete.count()
    deleted_users_ids = list(users_to_delete.values_list("id", flat=True))

    deleted_result = users_to_delete.delete()

    deleted_emails_count, _ = EmailAddress.objects.filter(
        verified=False
    ).delete()

    return {
        "deleted_users_count": deleted_users_count,
        "deleted_users_ids": deleted_users_ids,
        "delete_result": deleted_result,
        "deleted_unverified_emails_count": deleted_emails_count,
    }