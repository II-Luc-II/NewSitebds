from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Widget
from pylint.pyreverse.inspector import Project

from customer.models import Customer, MyProject, Documents, Fonctions, TicketMessage, Ticket


class CustomerAdmin(admin.StackedInline):
    model = Customer
    extra = 0


class CustomUserAdmin(UserAdmin):
    """Combine YogaCustomer et AccountBankCustomer sous UserAdmin."""
    inlines = [CustomerAdmin]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_per_page = 30
    list_max_show_all = 50


# Désenregistrer le modèle User par défaut pour éviter les conflits
admin.site.unregister(User)

# Enregistrer User avec notre CustomUserAdmin
admin.site.register(User, CustomUserAdmin)


@admin.register(MyProject)
class MyProjectAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'ref', 'project_name', 'status', 'created_at', 'project_type', 'domaine', 'server', 'created_at')
    list_filter = ('user', 'ref', 'project_name', 'project_type', 'domaine', 'server', 'created_at')
    search_fields = ('user__first_name', 'project_name', 'project_type', 'domaine', 'server', 'created_at')

    list_max_show_all = 50
    list_per_page = 30

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_name', 'created_at')
    list_filter = ('user', 'document_name', 'created_at')
    search_fields = ('user__first_name', 'document_name', 'created_at')
    list_max_show_all = 50
    list_per_page = 30


@admin.register(Fonctions)
class FonctionsAdmin(admin.ModelAdmin):
    list_display = (
    'project', 'auth_name', 'language_front', 'language_back', 'language_autre', 'planification', 'language_style',
    'nb_de_pages')
    list_filter = ('project__user',)
    search_fields = ('project__project_name',)
    list_max_show_all = 50
    list_per_page = 30


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "customer",
        "project",
        "ticket_type",
        "priority_badge",
        "status_badge",
        "created_at",
        "updated_at",
        "status",
    )

    list_filter = (
        "status",
        "priority",
        "ticket_type",
        "created_at",
        "project",
    )

    search_fields = (
        "title",
        "description",
        "customer__last_name",
        "customer__first_name",
        "customer__mail",
        "project__project_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "closed_at",
    )

    list_editable = (
        "status",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Client / Projet", {
            "fields": (
                "customer",
                "project",
            )
        }),
        ("Ticket", {
            "fields": (
                "title",
                "description",
                "ticket_type",
                "priority",
                "status",
                "attachment",
            )
        }),
        ("Dates", {
            "fields": (
                "created_at",
                "updated_at",
                "closed_at",
            )
        }),
    )

    def priority_badge(self, obj):
        colors = {
            "low": "secondary",
            "medium": "primary",
            "high": "warning",
            "urgent": "danger",
        }

        return format_html(
            '<span class="badge text-bg-{}">{}</span>',
            colors.get(obj.priority, "secondary"),
            obj.get_priority_display()
        )

    priority_badge.short_description = "Priorité"

    def status_badge(self, obj):
        colors = {
            "open": "success",
            "in_progress": "primary",
            "waiting_client": "warning",
            "resolved": "info",
            "closed": "secondary",
        }

        return format_html(
            '<span class="badge text-bg-{}">{}</span>',
            colors.get(obj.status, "secondary"),
            obj.get_status_display()
        )

    status_badge.short_description = "Statut"

    list_max_show_all = 50
    list_per_page = 30

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'created_at')

    list_max_show_all = 50
    list_per_page = 30

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }







