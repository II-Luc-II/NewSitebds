from django import forms

from .models import NewsletterSubscriber


from django import forms


class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Votre adresse e-mail",
                "autocomplete": "email",
            }
        ),
    )