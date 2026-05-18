# reservaciones/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtener valor de un diccionario por clave"""
    return dictionary.get(key, 0)