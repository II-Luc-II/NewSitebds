from django.contrib import admin
from django_ckeditor_5.fields import CKEditor5Widget
from django.utils.html import format_html
from django.db import models
from flechettes.models import Game

admin.site.site_header = 'Flechettes'
admin.site.site_title = "Administration de Flechettes"
admin.site.index_title = "Flechettes"



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'players_nbr_min', 'players_nbr_max', 'level', 'objectif', 'game_time', 'in_line', 'created_at')
    list_editable = ('players_nbr_min', 'players_nbr_max', 'level', 'objectif', 'game_time', 'in_line',)
    search_fields = ('name', 'players_nbr_min', 'players_nbr_max', 'level', 'objectif', 'game_time', 'created_at')

    list_max_show_all = 50
    list_per_page = 30

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }