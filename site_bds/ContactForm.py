from captcha.fields import CaptchaField
from django import forms

from site_bds.models import Contact, Newsletter
import re
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Contact, Newsletter


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        plain_message = strip_tags(message)

        # Longueur minimale
        if len(plain_message) < 20:
            raise ValidationError("Merci d’écrire un message plus détaillé (20 caractères minimum).")

        # Contenu indésirable
        bad_patterns = ["http", "viagra", "casino", "bitcoin", ".ru", ".xyz"]
        if any(pattern in plain_message.lower() for pattern in bad_patterns):
            raise ValidationError("Votre message contient du contenu interdit.")

        # Trop de liens ?
        if len(re.findall(r'https?://', plain_message.lower())) > 1:
            raise ValidationError("Merci de ne pas inclure plusieurs liens dans votre message.")

        return message  # très important !


class NewsLetterForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Newsletter
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        bad_domains = [".ru", ".xyz", "tempmail", "10minutemail", "mailinator"]

        if any(bad in email for bad in bad_domains):
            raise ValidationError("Veuillez utiliser un email valide et non temporaire.")
        return email


