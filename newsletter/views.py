from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods

from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscriber


def request_newsletter_subscription(request, email):
    """
    Crée ou récupère un abonné newsletter
    et envoie l'e-mail de confirmation si nécessaire.

    Retourne :
        subscriber,
        created,
        confirmation_sent
    """

    email = email.lower().strip()

    # -------------------------------------------------
    # Création / récupération de l'abonné
    # -------------------------------------------------
    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
    )

    # -------------------------------------------------
    # Déjà confirmé et actif
    # -------------------------------------------------
    if subscriber.is_confirmed and subscriber.is_active:
        return subscriber, created, False

    # -------------------------------------------------
    # URL de confirmation
    # -------------------------------------------------
    confirmation_url = request.build_absolute_uri(
        reverse(
            "newsletter:confirm",
            kwargs={
                "token": subscriber.confirmation_token,
            },
        )
    )

    # -------------------------------------------------
    # Contexte des templates e-mail
    # -------------------------------------------------
    context = {
        "confirmation_url": confirmation_url,
        "subscriber": subscriber,
    }

    # -------------------------------------------------
    # Génération des deux versions
    # -------------------------------------------------
    html_message = render_to_string(
        "emails/newsletter/confirmation.html",
        context,
    )

    text_message = render_to_string(
        "emails/newsletter/confirmation.txt",
        context,
    )

    # -------------------------------------------------
    # Création de l'e-mail
    # -------------------------------------------------
    email_message = EmailMultiAlternatives(
        subject="Confirmez votre inscription à la newsletter BDS",
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[subscriber.email],
    )

    # Version HTML
    email_message.attach_alternative(
        html_message,
        "text/html",
    )

    # -------------------------------------------------
    # Envoi
    # -------------------------------------------------
    email_message.send(
        fail_silently=False,
    )

    return subscriber, created, True


@require_POST
def subscribe(request):
    form = NewsletterSubscriptionForm(
        request.POST
    )

    if not form.is_valid():
        messages.error(
            request,
            "Veuillez saisir une adresse e-mail valide.",
        )

        return redirect(
            request.POST.get("next") or "/"
        )

    email = form.cleaned_data[
        "email"
    ]

    subscriber, created, confirmation_sent = (
        request_newsletter_subscription(
            request,
            email,
        )
    )

    if not confirmation_sent:
        messages.info(
            request,
            "Cette adresse e-mail est déjà inscrite "
            "à la newsletter.",
        )

    elif created:
        messages.success(
            request,
            "Un e-mail de confirmation vient de vous être envoyé.",
        )

    else:
        messages.success(
            request,
            "Un nouvel e-mail de confirmation vient de vous être envoyé.",
        )

    return redirect(
        request.POST.get("next") or "/"
    )


def confirm_subscription(request, token):
    subscriber = get_object_or_404(
        NewsletterSubscriber,
        confirmation_token=token,
    )

    if subscriber.is_confirmed and subscriber.is_active:

        messages.info(
            request,
            "Votre inscription à la newsletter est déjà confirmée.",
        )

    else:

        subscriber.confirm()

        messages.success(
            request,
            "Votre inscription à la newsletter est maintenant confirmée.",
        )

    return redirect("/")


@require_http_methods(["GET", "POST"])
def unsubscribe(request, token):
    subscriber = get_object_or_404(
        NewsletterSubscriber,
        unsubscribe_token=token,
    )

    if request.method == "POST":

        if subscriber.is_active:

            subscriber.unsubscribe()

            messages.success(
                request,
                "Vous êtes maintenant désinscrit de la newsletter.",
            )

        else:

            messages.info(
                request,
                "Cette adresse e-mail est déjà désinscrite.",
            )

        return redirect("/")

    return render(
        request,
        "unsubscribe_confirm.html",
        {
            "subscriber": subscriber,
        },
    )
