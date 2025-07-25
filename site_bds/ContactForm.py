from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from django import forms

from site_bds.models import Contact, Newsletter
import re
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Contact, Newsletter
from langdetect import detect, LangDetectException


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

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Détection de spam.")
        return ""

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        bad_domains = [".ru", ".xyz"]
        if any(email.endswith(domain) for domain in bad_domains):
            raise ValidationError("Les adresses emails avec ces domaines ne sont pas acceptées.")
        return email

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

        try:
            lang = detect(message)
        except LangDetectException:
            lang = None

        if lang and not lang.startswith("fr"):
            raise forms.ValidationError("Merci de rédiger votre message en français.")

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


class ContactFormPopUp(forms.ModelForm):
    captcha = CaptchaField()
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supprimer tous les labels
        for field in self.fields.values():
            field.label = ""

        # Config crispy pour ne pas afficher les labels
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        # Placeholder pour le captcha
        self.fields['captcha'].widget.attrs.update({'placeholder': 'Recopier le texte ci-dessus'})

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Spam détecté.")
        return ""

    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()

        # Vérifie longueur minimale
        if len(message) < 20:
            raise ValidationError("Merci d’écrire un message plus détaillé (20 caractères minimum).")

        # Vérifie contenu indésirable
        bad_patterns = ["http", "viagra", "casino", "bitcoin", ".ru", ".xyz"]
        if any(pattern in message.lower() for pattern in bad_patterns):
            raise ValidationError("Votre message contient du contenu interdit.")

        # Vérifie nombre de liens
        if len(re.findall(r'https?://', message.lower())) > 1:
            raise ValidationError("Merci de ne pas inclure plusieurs liens dans votre message.")

        return message

