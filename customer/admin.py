from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Widget

from customer.models import Customer, MyProject, Documents


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
    list_display = ('user', 'ref', 'project_name', 'status', 'created_at', 'project_type', 'domaine', 'server', 'created_at')
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