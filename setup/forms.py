from django import forms
from .models import academicyr,currentacademicyr,sclass,section,subjects,receipt_template,homework_time,birthday_wish_config,AppUpdate,StaffAnnouncement

receipt =[
    ('fee/reciept_show.html','Receipt1'),
    ('fee/reciept_show3.html','Receipt2')
]

class add_Acad_Form(forms.ModelForm):
    class Meta:
        model = academicyr
        fields = ('acad_year','school_name')
        labels = {
            'acad_year':'Academic Year',
        }
        widgets={
            'school_name':forms.HiddenInput(attrs={'class':'form-control'}),

            'acad_year': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family: Roboto, sans-serif; font-size: 16px; width: 100%;'
            }
        ),

        }


class set_current_yr(forms.ModelForm):
    class Meta:
        model = currentacademicyr
        fields = '__all__'

        widgets={
            'school_name':forms.HiddenInput()
        }

class add_class(forms.ModelForm):
    class Meta:
        model = sclass
        fields = ('name','acad_year','school_name')
        labels = {
            'name': 'Class Name :',
        }

        widgets = {
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family: Roboto, sans-serif; font-size: 16px; width: 80%;'}),

            'acad_year': forms.HiddenInput(attrs={'class':'form-control'}),
            'school_name': forms.HiddenInput(attrs={'class':'form-control'}),
        }

class add_section(forms.ModelForm):

    class Meta:
        model = section
        fields = '__all__'

        widgets = {
            'section_name': forms.TextInput(attrs={'class': 'pc-input'}),
            'class_sec_name': forms.HiddenInput(),
            'school_name': forms.HiddenInput(),
            'acad_year': forms.HiddenInput(),
        }


class add_subjects(forms.ModelForm):
    class Meta:
        model = subjects
        fields = '__all__'

        widgets = {
         'subject_name': forms.TextInput(attrs={'class':'form-control'}),
         'subject_code': forms.TextInput(attrs={'class':'form-control'}),
         'subject_year' : forms.HiddenInput(),
         'subject_class' : forms.HiddenInput(attrs={'class':'form-control'}),
         'subject_school' : forms.HiddenInput(),
        }



class receipt_template_form(forms.ModelForm):
    class Meta:
        model= receipt_template
        fields='__all__'
        widgets = {
            'template':forms.Select(choices=receipt,attrs={'class':'form-control'}),
            'school_name': forms.HiddenInput(),
        }
        
        
class add_homeworktime_form(forms.ModelForm):
    class Meta:
        model = homework_time
        fields = '__all__'

        widgets = {
            'time':forms.TimeInput(attrs={'class':'form-control','type': 'time'}),
            'homework_school': forms.HiddenInput()
        }


class birthday_wish_config_form(forms.ModelForm):
    class Meta:
        model = birthday_wish_config
        fields = '__all__'

        widgets = {
            'school': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Happy Birthday, {{student_name}}!'}),
            'message': forms.Textarea(attrs={
                'class': 'pc-input',
                'rows': 4,
                'placeholder': 'Use {{student_name}} to personalize. e.g. Wishing {{student_name}} a Happy Birthday!',
            }),
            'time': forms.TimeInput(attrs={'class': 'pc-input', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AppUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUpdate
        fields = ('title', 'description', 'date', 'badge', 'icon', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. Morning Report',
            }),
            'description': forms.Textarea(attrs={
                'class': 'pc-input',
                'rows': 3,
                'placeholder': 'Short description of the feature...',
            }),
            'date': forms.DateInput(attrs={
                'class': 'pc-input',
                'type': 'date',
            }),
            'badge': forms.Select(attrs={'class': 'pc-input'}),
            'icon': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. ri-star-line',
                'id': 'icon-input',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StaffAnnouncementForm(forms.ModelForm):
    class Meta:
        model = StaffAnnouncement
        fields = ['title', 'body', 'expires_on', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'Announcement title'}),
            'body': forms.Textarea(attrs={'class': 'pc-input', 'rows': 4, 'placeholder': 'Announcement details...'}),
            'expires_on': forms.DateInput(attrs={'class': 'pc-input', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
