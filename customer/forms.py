from django import forms
from pylint.pyreverse.inspector import Project

from customer.models import Customer, MyProject, Documents


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('last_name', 'first_name', 'entreprise', 'mail', 'phone', 'address', 'image')

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


class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'
