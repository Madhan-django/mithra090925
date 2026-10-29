from django import template
from django.contrib.auth.models import Group
from institutions.models import school

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

@register.simple_tag(takes_context=True)
def school_has_group_code(context, code):
    request = context.get('request')
    if not request:
        return False
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return False
    try:
        sch = school.objects.get(id=sch_id)
        return sch.group_code == code
    except school.DoesNotExist:
        return False
