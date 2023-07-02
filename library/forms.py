from django import forms
from .models import books,book_issued

status= [
    ('Issued','Issued'),
    ('returned','Returned')
]

class add_book_form(forms.ModelForm):
    class Meta:
        model = books
        fields='__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'issued': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'rack': forms.TextInput(attrs={'class': 'form-control'}),
            'book_no': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }

class add_bookissue_form(forms.ModelForm):
    class Meta:
        model = book_issued
        fields = '__all__'
        widgets = {
            'book_title': forms.Select(attrs={'class': 'form-control'}),
            'issued_to': forms.Select(attrs={'class': 'form-control'}),
            'sclass': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'acd_year': forms.Select(attrs={'class': 'form-control'}),
            'issued_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
