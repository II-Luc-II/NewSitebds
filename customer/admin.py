from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from customer.models import Customer


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