from django import forms
from .models import SchoolProfile, Banner, GalleryPhoto, PhotoGallery, VideoGallery

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


class GalleryPhotoForm(forms.Form):
    title    = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Annual Day Group Photo'}))
    album    = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Annual Day 2025'}))
    photo    = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'pc-input', 'accept': 'image/*'}))
    link_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'pc-input', 'placeholder': 'https://drive.google.com/... or YouTube link'}))
    is_active = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'pc-checkbox'}))


class PhotoGalleryForm(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        fields = ['PTitle', 'PThumbnail', 'Plink', 'Pdesc', 'Pdate', 'status']
        widgets = {
            'PTitle': forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Annual Day 2025'}),
            'PThumbnail': forms.URLInput(attrs={'class': 'pc-input', 'placeholder': 'https://... (thumbnail image URL)'}),
            'Plink': forms.URLInput(attrs={'class': 'pc-input', 'placeholder': 'https://drive.google.com/... or album URL'}),
            'Pdesc': forms.Textarea(attrs={'class': 'pc-input', 'rows': 3, 'placeholder': 'Short description (optional)'}),
            'Pdate': forms.DateInput(attrs={'class': 'pc-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'pc-input'}),
        }


class VideoGalleryForm(forms.ModelForm):
    class Meta:
        model = VideoGallery
        fields = ['VTitle', 'VThumbnail', 'Vlink', 'Vdesc', 'Vdate', 'status']
        widgets = {
            'VTitle': forms.TextInput(attrs={'class': 'pc-input', 'placeholder': 'e.g. Sports Day Highlights'}),
            'VThumbnail': forms.URLInput(attrs={'class': 'pc-input', 'placeholder': 'https://... (thumbnail image URL)'}),
            'Vlink': forms.URLInput(attrs={'class': 'pc-input', 'placeholder': 'https://youtube.com/... or video URL'}),
            'Vdesc': forms.Textarea(attrs={'class': 'pc-input', 'rows': 3, 'placeholder': 'Short description (optional)'}),
            'Vdate': forms.DateInput(attrs={'class': 'pc-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'pc-input'}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'link_url', 'is_active', 'display_order', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'pc-input',
                'placeholder': 'e.g. Annual Day 2025'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'pc-input'}),
            'link_url': forms.URLInput(attrs={
                'class': 'pc-input',
                'placeholder': 'https://... (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'pc-checkbox'}),
            'display_order': forms.NumberInput(attrs={
                'class': 'pc-input',
                'placeholder': '0'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'pc-input',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'pc-input',
                'type': 'date'
            }),
        }
