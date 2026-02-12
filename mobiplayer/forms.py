from django import forms
from .models import Video

sts = [
    ('Active','Active'),
    ('In-Active','In-Active')
]
class NewVideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

        labels= {
            'VTitle' : 'Title',
            'Vdesc' : 'Description',
            'Vdate' : 'Event Date',
            'status': 'Status',
            'Vlink' : 'Video URL'

        }

        widgets = {
            'VTitle': forms.TextInput(attrs= {'class': 'form-control','placeholder':'Title'}),
            'status': forms.Select(choices=sts,attrs={'class':'form-control'}),
            'Vpostdate': forms.HiddenInput(),
            'Vschool' : forms.HiddenInput(),
            'Vdesc': forms.Textarea(attrs={'class': 'form-control'}),
            'Vlink' : forms.TextInput(attrs={'class':'form-control'})

        }


