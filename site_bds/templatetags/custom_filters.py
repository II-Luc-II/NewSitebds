from django import template

register = template.Library()

@register.filter
def map_attribute(value, attribute):
    """
    Filtre pour extraire un attribut spécifique d'une liste de dictionnaires.
    """
    if isinstance(value, list):
        return [item.get(attribute) for item in value]
    return value