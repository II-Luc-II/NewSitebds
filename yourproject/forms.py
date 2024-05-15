from django import forms

from yourproject.models import Question


class QuestionForm(forms.ModelForm):
    QUESTION_1_CHOICES = (
        ('---------------', '---------------'),
        ('Application web', 'Application web'),
        ('Application Mobile', 'Application Mobile'),
        ('Site e-commerce', 'Site e-commerce'),
        ('Market_place', 'Market_place'),
        ('Site Vitrine', 'Site Vitrine'),
        ('Autre', 'Autre'),
    )
    QUESTION_2_CHOICES = (
        ('---------------', '---------------'),
        ('- 2 000 €', '- 2 000 €'),
        ('2 000 - 5 000 €', '2 000 - 5 000 €'),
        ('5 000 - 10 000 €', '5 000 - 10 000 €'),
        ('10 000 - 15 000 €', '10 000 - 15 000 €'),
        ('15 000 - 20 000 €', '15 000 - 20 000 €'),
        ('+ de 20 000€', '+ de 20 000€')
    )
    QUESTION_3_CHOICES = (
        ('---------------', '---------------'),
        ('Dès que possible', 'Dès que possible'),
        ('- de un mois', '- de un mois'),
        ('+ de 1 mois', '+ de 1 mois'),
    )

    questions_1 = forms.ChoiceField(choices=QUESTION_1_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    questions_2 = forms.ChoiceField(choices=QUESTION_2_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    questions_3 = forms.ChoiceField(choices=QUESTION_3_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ('questions_1', 'questions_2', 'questions_3', 'description', 'author', 'entreprise', 'email',
                  'telephone')

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description du projet'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du contact'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'entreprise'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
        }






