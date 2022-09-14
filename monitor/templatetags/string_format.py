from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def string_filter(string):
    try:
        return string.split(',')
    except Exception as e:
        error = e
        return string