from django.contrib import admin
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact, Newsletter, Blogs, ALaUne, PopUp, InfoLegacy, \
    PolicyLegacy, Article
from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Widget
from django.db import models

from yourproject.models import Question

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
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'job', 'is_published', 'display_image')
    list_editable = ('is_published', )

    def display_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="80" />')

    display_image.short_description = 'image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
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
            name = f'<span style="color:gray">&nbsp;{team.name}</span>'
            return format_html(yes_icon + name)
        else:
            name = f'<span style="color:red">&nbsp;{team.name}</span>'
            return format_html(no_icon + name)

    display_name.short_description = "Nom"

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" style="border-radius:8px;" />',
                obj.image.url
            )
        return "-"

    display_image.short_description = 'Image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(Ask)
class AskAdmin(admin.ModelAdmin):
    list_display = ('display_name', "created_at", "is_published")
    list_editable = ('is_published',)

    def display_name(self, ask):

        icon = "oui.png" if ask.is_published else "non.png"
        color = "gray" if ask.is_published else "red"

        return format_html(
            '<img src="/static/icons/{}" width="20" /> '
            '<span style="color:{};">{}</span>',
            icon,
            color,
            ask.ask
        )

    display_name.short_description = "Question"

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('display_name', "created_at", "checked", "no_robot")

    @staticmethod
    def display_name(contact):
        no_icon = '<img src="/static/icons/non.png" alt="False" style="width: 10px">'
        yes_icon = '<img src="/static/icons/oui.png" alt="True" style="width: 10px">'

        if contact.checked:
            name = '<span style="color:gray"> &nbsp;' + contact.name + '<span>'
            return format_html(yes_icon + name)
        else:
            name = '<span style="color:red"> &nbsp;' + contact.name + '<span>'
            return format_html(no_icon + name)

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


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
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(ALaUne)
class ALaUneAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'en_ligne')
    list_editable = ('en_ligne',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(PopUp)
class PopUpAdmin(admin.ModelAdmin):
    list_display = ('name', 'on_line', 'display_image', 'created_at')
    list_editable = ('on_line',)
    list_max_show_all = 50
    list_per_page = 30

    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="150" />')
        return ""

    display_image.short_description = 'Image'

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(InfoLegacy)
class InfoLegacyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(PolicyLegacy)
class PolicyLegacyAdmin(admin.ModelAdmin):
    list_display = ('titre', 'created_at')
    list_display_links = ('titre',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'display_image')
    list_display_links = ('title',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" style="border-radius:8px;" />',
                obj.image.url
            )
        return "-"

    display_image.short_description = 'Image'


