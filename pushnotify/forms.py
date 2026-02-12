from django import forms
from .models import GeneralNotification,SectionwiseNotification,SchoolNotification,temp_GeneralNotification

IS_Read= [
    (True, 'YES'),
    (False, 'NO'),
]

IS_Status= [
    ('Active','Active'),
    ('In-Active','In-Active'),
]

class New_General_Notification(forms.ModelForm):
    class Meta:
        model = temp_GeneralNotification
        fields = '__all__'
        labels = {
            'title': 'Title',
            'message' : 'Message',
            'create_date': 'Date',
            'post_date':'Scheduled Date',
            'post_to' : 'Students',
            'created_by' : 'Staff',
            'is_read': 'IS_Read',
            'status' : 'Status'


        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Message Title'}),
            'message': forms.Textarea(attrs={'class':'form-control','placeholder':'Message Title'}),
            'create_date': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
            'post_date': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
            'post_to': forms.SelectMultiple(attrs={'class':'form-control'}),
            'created_by_id': forms.HiddenInput(),
            'is_read': forms.HiddenInput(),
            'status': forms.Select(choices= IS_Status,attrs={'class':'form-control'}),
            'Notification_school':forms.HiddenInput(),
            'success_count':forms.HiddenInput(),
            'total_count': forms.HiddenInput()

        }
        
class section_Notification_form(forms.ModelForm):
    class Meta:
        model = SectionwiseNotification
        fields = '__all__'


class school_Notification_form(forms.ModelForm):
    class Meta:
        model = SchoolNotification
        fields = '__all__'