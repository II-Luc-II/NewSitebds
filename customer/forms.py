from django import forms

from customer.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('last_name', 'first_name','entreprise', 'mail', 'phone', 'address', 'complement_address', 'city', 'zip_code', 'image')

        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entreprise (Intitulé)'}),
            'mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            'complement_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "Complément de l'Adresse"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code Postal'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
