from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return ''

@register.filter(name='make_range')
def make_range(value):
    return range(value)
