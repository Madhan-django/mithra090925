from django import forms
from .models import LessonPlan, LessonPlanTopic, LessonPlanAssignment


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model  = LessonPlan
        fields = ['teacher', 'cls', 'section', 'subject', 'chapter']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'cls':     forms.Select(attrs={'class': 'form-select', 'id': 'id_cls'}),
            'section': forms.Select(attrs={'class': 'form-select', 'id': 'id_section'}),
            'subject': forms.Select(attrs={'class': 'form-select', 'id': 'id_subject'}),
            'chapter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chapter 3 – Fractions'}),
        }


class LessonPlanTopicForm(forms.ModelForm):
    class Meta:
        model  = LessonPlanTopic
        fields = ['topic', 'date', 'periods_required', 'teaching_method', 'status', 'objectives', 'content_taught']
        widgets = {
            'topic':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic name'}),
            'date':             forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'periods_required': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'teaching_method':  forms.Select(attrs={'class': 'form-select'}),
            'status':           forms.Select(attrs={'class': 'form-select'}),
            'objectives':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content_taught':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'periods_required': 'Periods Required',
        }


class LessonPlanAssignmentForm(forms.ModelForm):
    class Meta:
        model   = LessonPlanAssignment
        fields  = ['title', 'description', 'due_date']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date':    forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
