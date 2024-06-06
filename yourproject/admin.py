

from django.contrib import admin
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('author', 'entreprise', 'created_at', 'telephone', 'email')


admin.site.register(Question, QuestionAdmin)

