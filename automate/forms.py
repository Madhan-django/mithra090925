from django import forms
from .models import fee_automate_report,AutomateFunc

class fee_automate_form(forms.ModelForm):
    class Meta:
        model = fee_automate_report
        fields = '__all__'


class AutomateFuncForm(forms.ModelForm):
    class Meta:
        model = AutomateFunc
        fields = [
            'task',
            'schedule_type',
            'schedule_time',
            'automate_type',
            'send_to',
            'school',
            'created_by'

        ]
        widgets = {
            'schedule_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-select'}),
            'schedule_type': forms.Select(attrs={'class': 'form-select'}),
            'automate_type': forms.Select(attrs={'class': 'form-select'}),
            'send_to': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.HiddenInput(),
            'created_by':forms.HiddenInput()

        }

    def __init__(self, *args, **kwargs):
        super(AutomateFuncForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # make all fields required
