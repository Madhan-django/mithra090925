from django import forms
from timetable.models import TeachingAllocation,ReservedSlot

class TeachingAllocationForm(forms.ModelForm):
    class Meta:
        model = TeachingAllocation
        fields = ['teacher', 'subject', 'section', 'hours_per_week', 'teacher_school','cls','is_classteacher','not_first','not_last']
        widgets = {
            'hours_per_week': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'teacher_school':forms.HiddenInput()
        }

class EditTeachingAllocationForm(forms.ModelForm):
    class Meta:
        model = TeachingAllocation
        fields = ['teacher', 'subject', 'section', 'hours_per_week', 'teacher_school','cls','is_classteacher','not_first','not_last']
        widgets = {
            'hours_per_week': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'subject' : forms.HiddenInput(),
            'section': forms.HiddenInput(),
            'teacher': forms.HiddenInput(),
            'cls': forms.HiddenInput(),
            'not_first':forms.CheckboxInput(),
            'not_last':forms.CheckboxInput(),
            'teacher_school': forms.HiddenInput()

        }


class ReservedSlotForm(forms.ModelForm):
    class Meta:
        model = ReservedSlot
        fields = ['section', 'subject', 'timeslot', 'school','sch_class','adaptive_day','adaptive_period']
        widgets = {
            'sch_class':forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'timeslot': forms.Select(attrs={'class': 'form-control'}),
            'adaptive_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'adaptive_period': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'school': forms.HiddenInput()
        }

class EditReservedSlotForm(forms.ModelForm):
    class Meta:
        model = ReservedSlot
        fields = ['sch_class', 'section', 'subject', 'timeslot', 'school', 'adaptive_day', 'adaptive_period']
        widgets = {
            'sch_class': forms.HiddenInput(),
            'section': forms.HiddenInput(),
            'subject': forms.HiddenInput(),
            'timeslot': forms.Select(attrs={'class': 'form-control'}),
            'adaptive_day': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'adaptive_period': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'school': forms.HiddenInput(),
        }