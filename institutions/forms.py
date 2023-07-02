from django import forms
from .models import school


class add_school(forms.ModelForm):
    class Meta:
        model = school
        fields = ('name','phone','email','address','regno','isactive','logo')

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'regno': forms.TextInput(attrs={'class':'form-control'}),


        }


