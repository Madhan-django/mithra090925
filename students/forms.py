from django import forms
from .models import attendance,attendancegen,attendanceview


class addattendanceform(forms.ModelForm):
    class Meta:
        model = attendance
        fields = '__all__'



class attendancegen(forms.ModelForm):
    class Meta:
        model = attendancegen
        fields = '__all__'

        widgets = {
            'attndate':forms.DateInput(attrs={'class':'form-control','type':'date'}),
             'aclass':forms.Select(attrs={'class':'form-control'}),
             'sec':forms.Select(attrs={'class':'form-control'}),

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