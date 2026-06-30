from django import forms
from .models import SchoolProfile

class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = '__all__'
        widgets = {
            'school_name': forms.Select(attrs={
                'class': 'pc-input',
                'placeholder': 'Enter school name'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. Excellence in Education since 1978'
            }),
            'about': forms.Textarea(attrs={
                'class': 'pc-input',
                'rows': 4,
                'placeholder': 'Short description about the school'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'pc-input'
            }),
            'founder_name': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'Enter founder name'
            }),
            'founder_pic': forms.ClearableFileInput(attrs={
                'class': 'pc-input'
            }),
            'founded_year': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. 1978'
            }),
            'city': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. Chennai'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': '+91 44 2345 6789'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'pc-input',
                'placeholder': 'info@school.edu.in'
            }),
            'address': forms.Textarea(attrs={
                'class': 'pc-input',
                'rows': 3,
                'placeholder': 'Full address'
            }),
            'admission_open': forms.CheckboxInput(attrs={
                'class': 'pc-checkbox'
            }),
            'admission_url': forms.URLInput(attrs={
                'class': 'pc-input',
                'placeholder': 'https://yourschool.com/admission'
            }),
            'gallery_url': forms.URLInput(attrs={
                'class': 'pc-input',
                'placeholder': 'https://photos.google.com/...'
            }),
        }