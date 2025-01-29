
from django.contrib import admin
from .models import Visitor, Site, Vpn


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'date_visited')


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'status' )
    list_filter = ('status',)
    search_fields = ('name', 'url')


@admin.register(Vpn)
class VpnAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'url', 'status' )
    list_filter = ('status',)
    search_fields = ('name', 'url')