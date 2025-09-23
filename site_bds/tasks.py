
from celery import shared_task
from django.core.mail import send_mail

import logging
logger = logging.getLogger(__name__)

@shared_task
def send_mail_batch(subject, html_message, plain_message, recipient_batch, from_email):
    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_batch,
            html_message=html_message,
        )
        logger.info(f'Email envoyé à {recipient_batch}')
        return f'Email envoyé à {len(recipient_batch)} destinataires.'
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email : {e}")
        return f"Erreur lors de l'envoi de l'email : {e}"

