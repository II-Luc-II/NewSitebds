from django.contrib import admin
from site_stats.models import Visitor


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visitor_id', 'date_visited')


admin.site.register(Visitor, VisitorAdmin)