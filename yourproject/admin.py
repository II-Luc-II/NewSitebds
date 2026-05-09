
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from django.db import models
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('author', 'entreprise', 'email', 'telephone', 'created_at')
    list_display_links = ('author',)
    search_fields = ('author', 'entreprise', 'email', 'telephone', 'created_at')

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget}
    }




