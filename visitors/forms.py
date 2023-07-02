from django import forms
from .models import visitors

class add_visitorform(forms.ModelForm):
    class Meta:
        model = visitors
        fields = ['name', 'phone', 'email', 'company', 'address', 'purpose', 'meeting_person', 'photo','visitors_school','check_in_time','check_out_time']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_person': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'visitors_school': forms.Select(attrs={'class': 'form-control'}),
            'check_in_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'check_out_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
             'visitors_school':forms.HiddenInput(),
        }
