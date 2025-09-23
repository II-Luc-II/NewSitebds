from django import forms

from site_bds.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

        widgets = {

            'title': forms.TextInput(attrs={'class': 'form-control custom-text-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control custom-text-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control custom-text-input'}),

        }