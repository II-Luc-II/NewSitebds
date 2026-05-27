from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from site_bds.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'content': CKEditor5Widget(config_name='default'),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control custom-text-input'}),

        }