from django.contrib import admin
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact, Newsletter, Blogs, ALaUne
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget
from django.db import models

admin.site.site_header = 'SITE BDS Administration'


@admin.register(Gallery)
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


@admin.register(Testimonials)
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


@admin.register(Team)
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


@admin.register(Ask)
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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('display_name', "created_at", "checked", "no_robot")

    def display_name(self, contact):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if contact.checked:
            name = '<span style="color:gray"> &nbsp;' + contact.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + contact.name + '<span>'
            return format_html(no_icon + name)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'en_ligne', 'display_image', 'display_image_2', 'display_image_3', 'created_at')
    list_editable = ('en_ligne',)

    def display_image(self, obj):
        if obj.image:  # Vérification si l'image est présente
            return format_html(f'<img src="{obj.image.url}" width="150" />')
        return ""

    display_image.short_description = 'Image'

    def display_image_2(self, obj):
        if obj.image_2:  # Vérification si l'image_2 est présente
            return format_html(f'<img src="{obj.image_2.url}" width="150" />')
        return ""

    display_image_2.short_description = 'Image 2'

    def display_image_3(self, obj):
        if obj.image_3:  # Vérification si l'image_3 est présente
            return format_html(f'<img src="{obj.image_3.url}" width="150" />')
        return ""

    display_image_3.short_description = 'Image 3'

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(ALaUne)
class ALaUneAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'en_ligne')
    list_editable = ('en_ligne',)



