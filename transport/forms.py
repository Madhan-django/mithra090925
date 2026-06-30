from django import forms
from .models import VehicleType, Vehicle, Driver, Route, Stop, StudentTransport


class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model  = VehicleType
        fields = ['name', 'sch']
        widgets = {'sch': forms.HiddenInput()}


class VehicleForm(forms.ModelForm):
    class Meta:
        model  = Vehicle
        fields = [
            'sch', 'vehicle_number', 'vehicle_name', 'vehicle_type',
            'capacity', 'gps_device_id', 'chassis_number', 'engine_number',
            'fuel_type', 'purchase_date', 'rc_number',
            'insurance_expiry', 'fitness_expiry', 'permit_expiry', 'pollution_expiry',
            'status',
        ]
        widgets = {
            'sch':              forms.HiddenInput(),
            'purchase_date':    forms.DateInput(attrs={'type': 'date'}),
            'insurance_expiry': forms.DateInput(attrs={'type': 'date'}),
            'fitness_expiry':   forms.DateInput(attrs={'type': 'date'}),
            'permit_expiry':    forms.DateInput(attrs={'type': 'date'}),
            'pollution_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['vehicle_type'].queryset = VehicleType.objects.filter(sch=sch)


class DriverForm(forms.ModelForm):
    class Meta:
        model  = Driver
        fields = [
            'sch', 'name', 'employee_id', 'mobile', 'address',
            'aadhaar', 'license_number', 'license_expiry',
            'blood_group', 'emergency_contact', 'assigned_vehicle', 'status',
        ]
        widgets = {
            'sch':            forms.HiddenInput(),
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
            'address':        forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['assigned_vehicle'].queryset = Vehicle.objects.filter(sch=sch, status='Active')


class RouteForm(forms.ModelForm):
    class Meta:
        model  = Route
        fields = ['sch', 'route_name', 'route_code', 'vehicle', 'driver', 'total_distance', 'is_active']
        widgets = {'sch': forms.HiddenInput()}

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(sch=sch, status='Active')
            self.fields['driver'].queryset  = Driver.objects.filter(sch=sch, status='Active')


class StopForm(forms.ModelForm):
    class Meta:
        model  = Stop
        fields = ['stop_name', 'area', 'landmark', 'pickup_time', 'drop_time', 'sequence', 'monthly_fee']
        widgets = {
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'drop_time':   forms.TimeInput(attrs={'type': 'time'}),
        }


class StudentTransportForm(forms.ModelForm):
    class Meta:
        model  = StudentTransport
        fields = ['sch', 'student', 'route', 'stop', 'start_date', 'end_date', 'is_active']
        widgets = {
            'sch':        forms.HiddenInput(),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            from admission.models import students
            self.fields['student'].queryset = students.objects.filter(
                school_student=sch, student_status='active'
            ).order_by('first_name')
            self.fields['route'].queryset = Route.objects.filter(sch=sch, is_active=True)
            self.fields['stop'].queryset  = Stop.objects.filter(route__sch=sch)
