from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(str(key), '')
    return ''

@register.filter
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})