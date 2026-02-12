from django import forms
from .models import staff,staff_attendancegen,temp_homework

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
        exclude = ['staff_user']  # <- Exclude this field from the form
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),
            'status':forms.Select(choices=state),
            'gender':forms.Select(choices=gend,attrs={'class':'form-control','placeholder':'Gender'}),
            'dob':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile':forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.EmailInput(attrs={'class': 'form-control','type':'email','placeholder':'sample@gmail.com'}),
            'join':forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'salary':forms.NumberInput(attrs={'class': 'form-control'}),
            'desg':forms.TextInput(attrs={'class': 'form-control'}),
            'qualification':forms.TextInput(attrs={'class': 'form-control'}),
            'status':forms.Select(choices=state,attrs={ 'class':'select2 form-select','data-allow-clear':'true'}),
            'desc':forms.TextInput(attrs={'class': 'form-control'}),
            'staff_school':forms.HiddenInput(),
            'certifications':forms.TextInput(attrs={'class':'form-control'}),
            'experience':forms.TextInput(attrs={'class': 'form-control'}),
            'permission_group':forms.Select(choices=perm_group),
            'staff_photo':forms.FileInput(attrs={'class':'form-control','placeholder':'Staff Photograph'}),
            'subjects_taught':forms.MultipleHiddenInput()
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
        model = temp_homework
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
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'})
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


class edit_homework_form(forms.ModelForm):
    class Meta:
        model = temp_homework
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'hclass': forms.HiddenInput(),
            'secs': forms.HiddenInput(),
            'subj': forms.HiddenInput(),
            'homework_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'submission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'created_by': forms.HiddenInput(),
            'acad_yr': forms.HiddenInput(),
            'school_homework': forms.HiddenInput(),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'})
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