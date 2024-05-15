from django import forms

from site_bds.models import Contact, Newsletter


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


