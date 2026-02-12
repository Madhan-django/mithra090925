from django import forms
from .models import BioDevices,BioShift,BioDept,Employee

status=[
    ('Working','Working'),
    ('Resigned','Resigned')
]

class AttendanceDateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Select Date'
    )

class NewBioDeviceForm(forms.ModelForm):
    class Meta:
        model = BioDevices
        fields = '__all__'
        widgets = {
            'BioName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter device name'}),
            'BioLocation': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter device description'}),
            'BioSerial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter serial number'}),
            'BioSchool': forms.HiddenInput()
            # Add widgets for other fields as needed
        }
        labels = {
            'BioName': 'Device Name',
            'BioLocation': 'Description',
            'BioSerial': 'Serial Number',
            # Add labels for other fields as needed
        }


    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        # Add custom validation if needed
        if BioDevices.objects.filter(serial_number=serial_number).exists():
            raise forms.ValidationError("This serial number is already in use.")
        return serial_number

class BioShiftForm(forms.ModelForm):
    class Meta:
        model = BioShift
        fields='__all__'

        widgets = {
            'DeptName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Shift Name'}),
            'ShiftStartTime': forms.TimeInput(),
            'ShiftEndTime': forms.TimeInput(),
            'ShiftSchool': forms.HiddenInput()
            # Add widgets for other fields as needed
        }
        labels = {
            'DeptName': 'Department',
            'ShiftStartTime': 'Start',
            'ShiftEndTime': 'End Time',
            # Add labels for other fields as needed
        }

class BioDeptForm(forms.ModelForm):
    class Meta:
        model = BioDept
        fields='__all__'

        widgets = {
            'DeptName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department Name'}),
            'ShiftDet': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Shift'}),
            'DeptSchool': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Shift'}),
            # Add widgets for other fields as needed
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'EmployeeId',
            'EmployeeName_id',
            'EmployeeCode',
            'StringCode',
            'NumericCode',
            'Gender',
            'CompanyId',
            'DepartmentId',
            'Dept',
            'CategoryId',
            'DOJ',
            'EmployeeCodeInDevice',
            'EmployementType',
            'Status',
            'RecordStatus',
            'EmpSchool'
        ]
        widgets = {
            'Status': forms.Select(choices=status,attrs={'class': 'form-control', 'placeholder': 'Select Shift'}),
            'DOJ':forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
                        # Add widgets for other fields as needed
        }
