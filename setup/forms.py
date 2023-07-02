from django import forms
from .models import academicyr,currentacademicyr,sclass,section,subjects



class add_Acad_Form(forms.ModelForm):
    class Meta:
        model = academicyr
        fields = ('acad_year','school_name')
        labels = {
            'acad_year':'Academic Year',
        }
        widgets={
            'school_name':forms.HiddenInput(attrs={'class':'form-control'})
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
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'acad_year': forms.HiddenInput(attrs={'class':'form-control'}),
            'school_name': forms.HiddenInput(attrs={'class':'form-control'}),
        }

class add_section(forms.ModelForm):

    class Meta:
        model = section
        fields = '__all__'



        widgets = {
                    'section_name':forms.TextInput(attrs={'class':'form-control'}),
                    'class_sec_name':forms.Select(attrs={'class':'form-control'}),
                    'school_name':forms.HiddenInput(attrs={'class':'form-control'}),
                    'acad_year': forms.HiddenInput(attrs={'class': 'form-control'}),
                }


class add_subjects(forms.ModelForm):
    class Meta:
        model = subjects
        fields = '__all__'

        widgets = {
         'subject_name': forms.TextInput(attrs={'class':'form-control'}),
         'subject_code': forms.TextInput(attrs={'class':'form-control'}),
         'subject_year' : forms.HiddenInput(),
         'subject_class' : forms.Select(attrs={'class':'form-control'}),
         'subject_school' : forms.HiddenInput(),
        }



