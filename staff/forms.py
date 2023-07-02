from django import forms
from .models import staff,staff_attendancegen,homework

state= [
    ('Active','Active'),
    ('In-Active','In-Active'),

]
perm_group=[
    ('admin','Admin'),
    ('Teacher','Teacher'),
]
gend = [
    ('Male','Male'),
    ('Female','Female'),
    ('Transgender','Transgender'),
]
class add_staff_form(forms.ModelForm):
    class Meta:
        model = staff
        fields='__all__'
        widgets = {
            'staff_name':forms.TextInput(attrs={'class': 'form-control col-sm-3'}),
            'status':forms.Select(choices=state),
            'gender':forms.Select(choices=gend),
            'dob':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile':forms.TextInput(attrs={'class': 'form-control col-sm-3'}),
            'email':forms.EmailInput(attrs={'class': 'form-control col-sm-4'}),
            'join':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'Role': forms.TextInput(attrs={'class': 'form-control col-sm-4'}),
            'salary':forms.NumberInput(),
            'desg':forms.TextInput(attrs={'class': 'form-control'}),
            'qualification':forms.TextInput(attrs={'class': 'form-control'}),
            'status':forms.Select(choices=state),
            'desc':forms.TextInput(attrs={'class': 'form-control'}),
            'staff_school':forms.HiddenInput(),
            'country':forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'state':forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'city':forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'zip_code':forms.TextInput(attrs={'class': 'form-control col-sm-2'}),
            'education':forms.TextInput(attrs={'class': 'form-control'}),
            'certifications':forms.TextInput(attrs={'class': 'form-control'}),
            'experience':forms.TextInput(attrs={'class': 'form-control'}),
            'skills':forms.TextInput(attrs={'class': 'form-control'}),
            'permission_group':forms.Select(choices=perm_group),
            'user':forms.Select(),
        }
        labels = {
            'desg':'Designation',
            'desc':'Description',

        }



class add_staff_attendance_gen(forms.ModelForm):
    class Meta:
        model = staff_attendancegen
        fields = '__all__'

        labels = {
            'attndate': 'Date'
        }

        widgets = {
            'staff_school':forms.HiddenInput(),

            'attndate':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
        }


class add_homework_form(forms.ModelForm):
    class Meta:
        model = homework
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'hclass': forms.Select(attrs={'class': 'form-control'}),
            'secs': forms.Select(attrs={'class': 'form-control'}),
            'subj': forms.Select(attrs={'class': 'form-control'}),
            'homework_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'submission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
             'acad_yr':forms.HiddenInput(),
            'school_homework': forms.HiddenInput(),
        }

        labels = {
            'title': 'Homework Title',
            'hclass': 'Class',
            'secs': 'Section',
            'subj': 'Subject',
            'homework_date': 'Homework Date',
            'description': 'Description',
            'submission_date': 'Submission Date',
            'created_by': 'Created By',

        }


