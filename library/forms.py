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

        labels = {
            'title': 'Title',
            'author': 'Author',
            'subject': 'Subject',
            'price': 'Price',
            'quantity': 'Quantity',
            'issued': 'Issued',
            'desc': 'Description',
            'rack': 'Rack No',
            'book_no': 'Book No',
            'isbn': 'ISBN No',

        }

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
            'book_school':forms.HiddenInput()
        }

        def __init__(self, *args, **kwargs):
            super(AddBookForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.label_tag(attrs={'class': 'form-label'})

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
