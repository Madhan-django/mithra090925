from django import forms
from .models import LessonPlan, LessonPlanAssignment


class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = [
            'teacher', 'subject', 'cls', 'section',
            'date', 'period_number',
            'chapter', 'topic',
            'objectives', 'content_taught',
            'teaching_method', 'status',
        ]
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'cls': forms.Select(attrs={'class': 'form-select', 'id': 'id_cls'}),
            'section': forms.Select(attrs={'class': 'form-select', 'id': 'id_section'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'chapter': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content_taught': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'teaching_method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class LessonPlanAssignmentForm(forms.ModelForm):
    class Meta:
        model = LessonPlanAssignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
