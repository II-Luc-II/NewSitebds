from django.contrib import admin
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from django.urls import reverse
from django.db import models

admin.site.site_header = 'SITE BDS Administration'


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('display_name', "display_image", "is_published")
    list_editable = ('is_published',)

    def display_name(self, gallery):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if gallery.is_published:
            name = '<span style="color:gray"> &nbsp;' + gallery.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + gallery.name + '<span>'
            return format_html(no_icon + name)

    def display_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="150" />')

    display_image.short_description = 'image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'job', 'is_published', 'display_image')
    list_editable = ('is_published', )

    def display_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="80" />')

    display_image.short_description = 'image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

    def display_name(self, gallery):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if gallery.is_published:
            name = '<span style="color:gray"> &nbsp;' + gallery.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + gallery.name + '<span>'
            return format_html(no_icon + name)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('display_name', "function", "display_image", "is_published")
    list_editable = ('is_published',)

    def display_name(self, team):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if team.is_published:
            name = '<span style="color:gray"> &nbsp;' + team.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + team.name + '<span>'
            return format_html(no_icon + name)

    def display_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="150" />')

    display_image.short_description = 'image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class AskAdmin(admin.ModelAdmin):
    list_display = ('display_name', "created_at", "is_published")
    list_editable = ('is_published',)

    def display_name(self, ask):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 20px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 20px">'

        if ask.is_published:
            name = '<span style="color:gray"> &nbsp;' + ask.ask + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + ask.ask + '<span>'
            return format_html(no_icon + name)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


class ContactAdmin(admin.ModelAdmin):
    list_display = ('display_name', "created_at", "checked")

    def display_name(self, contact):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if contact.checked:
            name = '<span style="color:gray"> &nbsp;' + contact.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + contact.name + '<span>'
            return format_html(no_icon + name)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Ask, AskAdmin)
admin.site.register(Contact, ContactAdmin)

