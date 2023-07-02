from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.simple_tag(takes_context=True)
def hide_menu_for_group(context, group_name):
    user = context['request'].user
    if user.is_authenticated and user.groups.filter(name=group_name).exists():
        return ' '
    return ''

@register.simple_tag
def end_hide_menu_for_group():
    return ''
