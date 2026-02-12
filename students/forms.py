from django import forms
from .models import attendance,attendancegen,attendanceview


class addattendanceform(forms.ModelForm):
    class Meta:
        model = attendance
        fields = '__all__'

        widgets= {
            'aclass':forms.TextInput(attrs={'class':'form-control','style':'height:50px;'}),
            'sec': forms.TextInput(attrs={'class': 'form-control', 'style': 'height:50px;'}),
        }



class attendancegen(forms.ModelForm):
    class Meta:
        model = attendancegen
        fields = '__all__'

        widgets = {
            'attndate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'height:50px;'}),
            'aclass': forms.Select(attrs={'class': 'form-control', 'style': 'height:50px;'}),
            'sec': forms.Select(attrs={'class': 'form-control', 'style': 'height:50px;'}),
        }

class attendanceview(forms.ModelForm):
    class Meta:
        model = attendanceview
        fields = '__all__'
        widgets = {
            'attndate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'aclass': forms.Select(attrs={'class': 'form-control'}),
            'sec': forms.Select(attrs={'class': 'form-control'}),

        }
