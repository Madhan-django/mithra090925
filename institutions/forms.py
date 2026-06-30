from django import forms
from .models import school



class add_school(forms.ModelForm):
    class Meta:
        model = school
        fields = '__all__'


