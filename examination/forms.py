from django import forms
from .models import exams,exam_subjectmap,temp_insert,exam_result
from django.forms import inlineformset_factory

class add_exam_form(forms.ModelForm):
    class Meta:
        model = exams
        fields='__all__'

        widgets = {
            'exam_title': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_code': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_centre': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_class': forms.Select(attrs={'class': 'form-control'}),
            'exam_Sub_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_groupby': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_start_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'exam_end_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'exam_year': forms.Select(attrs={'class': 'form-control'}),
            'exam_school': forms.HiddenInput()
        }

class add_exam_subjectmap_form(forms.ModelForm):
    class Meta:
        model = exam_subjectmap
        fields='__all__'
        widgets = {
            'exname': forms.Select(attrs={'class': 'form-control'}),
            'exam_subjects': forms.Select(attrs={'class': 'form-control'}),
            'exam_subject_type': forms.TextInput(attrs={'class': 'form-control'}),
            'paper_code': forms.TextInput(attrs={'class': 'form-control'}),
            'paper_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_no': forms.TextInput(attrs={'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class temp_insert_form(forms.ModelForm):
    class Meta:
        model = temp_insert
        fields ='__all__'

class exam_resultform(forms.ModelForm):
    class Meta:
        model = exam_result
        fields = ('obtained_marks','exam_sub','adm_card','remark')
        labels = {
            'obtained_marks': 'Marks',
            'exam_sub': 'Subjects',
        }