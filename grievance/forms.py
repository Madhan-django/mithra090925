from django import forms
from .models import Grievance

class GrievanceForm(forms.ModelForm):

    complaint_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    action_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Grievance
        fields = '__all__'

        widgets = {
            'gschool': forms.HiddenInput(),
            'gclass': forms.Select(attrs={'class': 'form-select'}),
            'gsec': forms.Select(attrs={'class': 'form-select'}),
            'stud_name': forms.Select(attrs={'class': 'form-select'}),
            'ac_year': forms.HiddenInput(),

            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 10-digit mobile number'
            }),

            'area_of_complaint': forms.Select(attrs={'class': 'form-select'}),

            'aoc_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify if Other'
            }),

            'detail': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write details (max 250 characters)'
            }),
            'no_action_taken':forms.HiddenInput(),
            'principal_remark': forms.TextInput(attrs={'class': 'form-control'}),
            'concern_person_remark': forms.TextInput(attrs={'class': 'form-control'}),
            'act_details': forms.TextInput(attrs={'class': 'form-control'}),

            'act_intimation_to_person': forms.Select(attrs={'class': 'form-select'}),
            'complaint_status': forms.Select(attrs={'class': 'form-select'}),
            'complaint_received': forms.Select(attrs={'class': 'form-select'}),

            'concern_person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter concern person name'
            }),
        }

class GrievanceupdateForm(forms.ModelForm):
    complaint_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )

    action_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Grievance
        fields = '__all__'
        widgets = {
            'gschool': forms.HiddenInput(),
            'ac_year': forms.HiddenInput(),

            # Hide gsec and aoc_other
            'gsec': forms.HiddenInput(),
            'aoc_other': forms.HiddenInput(),
            'no_action_taken':forms.HiddenInput(),
            'gclass': forms.HiddenInput(),
            'stud_name': forms.HiddenInput(),
            'mobile': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'area_of_complaint': forms.HiddenInput(),
            'detail': forms.Textarea(attrs={'class': 'form-control','readonly': 'readonly'}),
            'principal_remark': forms.TextInput(attrs={'class': 'form-control'}),
            'concern_person_remark': forms.TextInput(attrs={'class': 'form-control'}),
            'act_details': forms.TextInput(attrs={'class': 'form-control'}),
            'act_intimation_to_person': forms.Select(attrs={'class': 'form-select'}),
            'complaint_status': forms.Select(attrs={'class': 'form-select'}),
            'complaint_received': forms.HiddenInput(),
            'concern_person_name': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
        }