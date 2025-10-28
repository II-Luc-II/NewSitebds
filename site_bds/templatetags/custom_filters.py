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


from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def zip(value, arg):
    """
    Permet d'associer deux listes ensemble dans le template.
    """
    try:
        return zip(value, arg)
    except TypeError:
        return []



@register.filter
def get_dict_value(dictionary, key):
    """ Récupère une valeur d'un dictionnaire à partir d'une clé """
    return dictionary.get(key, None)