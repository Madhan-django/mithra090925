from django import template
from examination.models import GradeScale

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Lookup a dict by key in templates: {{ my_dict|get_item:key }}"""
    return dictionary.get(key)


@register.simple_tag
def get_grade(obtained, max_marks, school_id):
    """Return the grade letter for obtained/max_marks based on school grade scale."""
    if obtained is None or not max_marks:
        return '-'
    try:
        pct = (float(obtained) / float(max_marks)) * 100
        grade = GradeScale.objects.filter(
            school_id=school_id,
            min_percent__lte=pct,
            max_percent__gte=pct
        ).first()
        return grade.grade if grade else '-'
    except (TypeError, ZeroDivisionError):
        return '-'


@register.simple_tag
def get_grade_point(obtained, max_marks, school_id):
    """Return the grade point for obtained/max_marks based on school grade scale."""
    if obtained is None or not max_marks:
        return '-'
    try:
        pct = (float(obtained) / float(max_marks)) * 100
        grade = GradeScale.objects.filter(
            school_id=school_id,
            min_percent__lte=pct,
            max_percent__gte=pct
        ).first()
        return grade.grade_point if grade else '-'
    except (TypeError, ZeroDivisionError):
        return '-'
