from django.contrib import admin, messages
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils import timezone
from django.utils.html import strip_tags, format_html

from .models import Newsletter, NewsletterSubscriber, NewsletterDelivery
from django_ckeditor_5.widgets import CKEditor5Widget
from django.db.models import Count, Q




@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "is_confirmed",
        "is_active",
        "created_at",
        "confirmed_at",
        "unsubscribed_at",
    )

    list_filter = (
        "is_confirmed",
        "is_active",
        "created_at",
        "confirmed_at",
        "unsubscribed_at",
    )

    search_fields = (
        "email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "confirmation_token",
        "unsubscribe_token",
        "created_at",
        "confirmed_at",
        "unsubscribed_at",
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "status",
        "sent_count",
        "failed_count",
        "created_at",
        "sent_at",
        "preview_link",
    )

    list_filter = (
        "status",
        "created_at",
        "sent_at",
    )

    search_fields = (
        "subject",
        "content",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "sent_at",
        "preview_link",
    )

    actions = [
        "send_newsletters",
        "retry_failed_deliveries",
    ]

    # =========================================================
    # COMPTEURS D'ENVOI
    # =========================================================

    @admin.display(
        description="Envoyés",
        ordering="sent_count_annotation",
    )
    def sent_count(self, obj):
        return obj.sent_count_annotation

    @admin.display(
        description="Échecs",
        ordering="failed_count_annotation",
    )
    def failed_count(self, obj):
        return obj.failed_count_annotation

    # =========================================================
    # QUERYSET
    # =========================================================

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.annotate(
            sent_count_annotation=Count(
                "deliveries",
                filter=Q(
                    deliveries__status=NewsletterDelivery.Status.SENT,
                ),
            ),
            failed_count_annotation=Count(
                "deliveries",
                filter=Q(
                    deliveries__status=NewsletterDelivery.Status.FAILED,
                ),
            ),
        )

    # =========================================================
    # URL APERÇU
    # =========================================================

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:newsletter_id>/preview/",
                self.admin_site.admin_view(
                    self.preview_newsletter
                ),
                name="newsletter_newsletter_preview",
            ),
        ]

        return custom_urls + urls

    # =========================================================
    # BOUTON APERÇU
    # =========================================================

    @admin.display(
        description="Aperçu"
    )
    def preview_link(self, obj):

        if not obj or not obj.pk:
            return "-"

        url = reverse(
            "admin:newsletter_newsletter_preview",
            args=[obj.pk],
        )

        return format_html(
            '<a class="button" href="{}" target="_blank">'
            'Voir l’aperçu'
            "</a>",
            url,
        )

    # =========================================================
    # PAGE APERÇU
    # =========================================================

    def preview_newsletter(
        self,
        request,
        newsletter_id,
    ):

        newsletter = self.get_object(
            request,
            newsletter_id,
        )

        if newsletter is None:
            from django.http import Http404
            raise Http404

        logo_url = request.build_absolute_uri(
            "/static/assets/images/Logo-arbre-genealogique.png"
        )

        context = {
            **self.admin_site.each_context(request),
            "newsletter": newsletter,
            "logo_url": logo_url,
            "title": f"Aperçu : {newsletter.subject}",
        }

        return TemplateResponse(
            request,
            "admin/newsletter/newsletter/preview.html",
            context,
        )

    # =========================================================
    # ACTION : ENVOYER
    # =========================================================

    @admin.action(
        description="Envoyer les newsletters sélectionnées"
    )
    def send_newsletters(self, request, queryset):

        subscribers = NewsletterSubscriber.objects.filter(
            is_active=True,
            is_confirmed=True,
        )

        if not subscribers.exists():
            self.message_user(
                request,
                "Aucun abonné actif et confirmé.",
                level=messages.WARNING,
            )
            return

        newsletters = queryset.exclude(
            status__in=[
                Newsletter.Status.QUEUED,
                Newsletter.Status.SENT,
            ],
        )

        if not newsletters.exists():
            self.message_user(
                request,
                (
                    "Les newsletters sélectionnées sont déjà "
                    "en attente d'envoi ou ont déjà été envoyées."
                ),
                level=messages.WARNING,
            )
            return

        base_url = request.build_absolute_uri("/").rstrip("/")

        queued = 0

        for newsletter in newsletters:

            # -------------------------------------------------
            # Verrouillage avant l'ajout dans Celery
            # -------------------------------------------------

            updated = (
                Newsletter.objects
                .filter(
                    pk=newsletter.pk,
                )
                .exclude(
                    status__in=[
                        Newsletter.Status.QUEUED,
                        Newsletter.Status.SENT,
                    ],
                )
                .update(
                    status=Newsletter.Status.QUEUED,
                )
            )

            # Newsletter déjà prise en charge.
            if updated == 0:
                continue

            # -------------------------------------------------
            # Ajout dans la file Celery
            # -------------------------------------------------

            try:
                send_newsletter_task.delay(
                    newsletter.id,
                    base_url,
                )

            except Exception:

                # Redis / Celery indisponible :
                # retour au statut brouillon.
                Newsletter.objects.filter(
                    pk=newsletter.pk,
                    status=Newsletter.Status.QUEUED,
                ).update(
                    status=Newsletter.Status.DRAFT,
                )

                raise

            queued += 1

        # -----------------------------------------------------
        # MESSAGE ADMIN
        # -----------------------------------------------------

        if queued == 0:
            self.message_user(
                request,
                (
                    "Aucune newsletter n'a été ajoutée "
                    "à la file d'envoi."
                ),
                level=messages.WARNING,
            )
            return

        self.message_user(
            request,
            (
                f"{queued} newsletter(s) placée(s) "
                "dans la file d'envoi."
            ),
            level=messages.SUCCESS,
        )

    @admin.action(
        description="Réessayer les envois en échec"
    )
    def retry_failed_deliveries(
            self,
            request,
            queryset,
    ):

        base_url = request.build_absolute_uri("/").rstrip("/")

        queued = 0

        for newsletter in queryset:

            has_failed = newsletter.deliveries.filter(
                status=NewsletterDelivery.Status.FAILED,
            ).exists()

            if not has_failed:
                continue

            retry_failed_newsletter_deliveries.delay(
                newsletter.id,
                base_url,
            )

            queued += 1

        if queued == 0:
            self.message_user(
                request,
                "Aucun envoi en échec à réessayer.",
                level=messages.WARNING,
            )
            return

        self.message_user(
            request,
            (
                f"Relance des échecs programmée pour "
                f"{queued} newsletter(s)."
            ),
            level=messages.SUCCESS,
        )