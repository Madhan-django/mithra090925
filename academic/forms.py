from django import forms
from .models import noticeboard
sts = (
    ('Active','Active'),
    ('In-Active', 'In-Active'),
)

class NoticeBoardForm(forms.ModelForm):
    class Meta:
        model = noticeboard
        fields = ('title', 'notice_date', 'content', 'file', 'url', 'status', 'notice_school')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'notice_date': forms.DateInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=sts,attrs={'class': 'form-control'}),
            'notice_school': forms.HiddenInput(),
        }


from django import forms
from .models import events

class add_event_form(forms.ModelForm):
    class Meta:
        model = events
        fields = ('event_title', 'event_desc', 'start_date', 'end_date', 'event_location', 'event_image', 'event_school')
        widgets = {
            'event_title': forms.TextInput(attrs={'class': 'form-control'}),
            'event_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'start_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'end_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'event_location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'event_school': forms.HiddenInput(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            instance = kwargs.get('instance')
            if instance:
                self.fields['event_image'].initial = instance.event_image