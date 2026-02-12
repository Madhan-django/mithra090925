from django import forms
from .models import school



class add_school(forms.ModelForm):

    class Meta:
        model = school

        fields = (
            'name', 'phone', 'email', 'address', 'regno', 'isactive',
            'logo', 'notification_logo', 'website',
            'web_aboutus', 'web_contactus', 'web_gallery', 'web_admission'
        )

        labels = {
            'web_aboutus': 'About Us',
            'web_contactus': 'Contact Us',
            'web_gallery': 'Gallery',
            'web_admission': 'Admission',
        }

        widgets = {

            # ===== BASIC DETAILS =====
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'regno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'website': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            # ===== STATUS =====
            'isactive': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'transform: scale(1.5); margin-top: 8px;'
            }),

            # ===== FILE UPLOADS =====
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'notification_logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            # ===== WEB CONTENT =====
            'web_aboutus': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'web_contactus': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'web_gallery': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),

            'web_admission': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': ' ',
                'style': 'font-family: Roboto, sans-serif; font-size: 18px;'
            }),
        }
