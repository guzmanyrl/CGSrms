from django import template
import os 
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, attrs):
    """Add HTML attributes to a Django form field."""
    # Ensure 'field' has both 'field' and 'widget' attributes to prevent AttributeError
    if hasattr(field, 'field') and hasattr(field.field, 'widget'):
        for attr in attrs.split(','):
            key, value = attr.split('=')
            field.field.widget.attrs[key.strip()] = value.strip().strip('"')
    return field

@register.filter
def basename(value):
    """Returns the base name of a file path."""
    return os.path.basename(value)

@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve item from a dictionary."""
    if isinstance(dictionary, list) and isinstance(key, int):
        return dictionary[key]  # Access list by index
    if isinstance(dictionary, dict):
        return dictionary.get(key)  # Access dictionary by key
    return None

@register.filter
def add_attrs(field, attrs):
    """
    Adds attributes to form fields dynamically in templates.
    """
    try:
        # Parse the attributes string
        attr_dict = dict(attr.split('=') for attr in attrs.split(' '))
        return field.as_widget(attrs=attr_dict)
    except ValueError:
        raise ValueError("Ensure attributes are formatted correctly: key='value' pairs separated by spaces.")