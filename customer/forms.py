from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from pylint.pyreverse.inspector import Project
from allauth.account.forms import SignupForm
from customer.models import Customer, MyProject, Documents, Ticket, TicketMessage


class CustomerForm(forms.ModelForm):
    agree_terms = forms.BooleanField(
        required=True,
        label="J'accepte la politique de confidentialité (RGPD)",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    class Meta:
        model = Customer
        fields = ('last_name', 'first_name', 'entreprise', 'mail', 'phone', 'address', 'image', 'agree_terms',)

        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entreprise (Intitulé)'}),
            'mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('user', 'last_name', 'first_name', 'entreprise', 'mail', 'phone', 'address', 'image')

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entreprise (Intitulé)'}),
            'mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = MyProject
        fields = [
            "user",
            "project_name",
            "project_type",
            "status",
            "domaine",
            "server",
            "maintenance_contract",
            "description",
        ]

        widgets = {
            "user": forms.Select(attrs={
                "class": "form-control custom-text-input"
            }),
            "project_name": forms.TextInput(attrs={
                "class": "form-control custom-text-input"
            }),
            "project_type": forms.Select(attrs={
                "class": "form-control custom-text-input"
            }),
            "status": forms.Select(attrs={
                "class": "form-control custom-text-input"
            }),
            "domaine": forms.TextInput(attrs={
                "class": "form-control custom-text-input"
            }),
            "server": forms.TextInput(attrs={
                "class": "form-control custom-text-input"
            }),
            "maintenance_contract": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "description": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5"
                },
                config_name="default"
            ),
        }


class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'


class TicketClientForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "project",
            "title",
            "description",
            "ticket_type",
            "priority",
            "attachment",
        ]

        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Décrivez votre demande..."
            }),
        }

    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)

        if customer:
            self.fields["project"].queryset = MyProject.objects.filter(user=customer)

        self.fields["project"].required = False


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ["message", "attachment"]

        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Écrire une réponse..."
            }),
        }
