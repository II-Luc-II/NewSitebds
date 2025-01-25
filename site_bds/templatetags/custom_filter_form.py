from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter
def add_class(field, css_class):
    # Vérifiez si le champ est une instance de BoundField
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    # Sinon, retournez l'objet tel quel pour éviter l'erreur
    return field
