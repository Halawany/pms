# pms/templatetags/form_filters.py

from django import template

register = template.Library()

# Custom filter to add a class to a form field
@register.filter
def add_class(value, css_class):
    """Adds a CSS class to a form field"""
    return value.as_widget(attrs={'class': css_class})
