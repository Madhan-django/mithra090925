from django import forms
from .models import (
    Hostel, Block, Floor, Room, Bed, HostelAdmission,
    RoomTransfer, WaitingList, HostelFeeType, HostelFeeInvoice,
    HostelFeeReceipt, HostelAttendance, LeaveApplication, GatePass,
)
from admission.models import students
from setup.models import academicyr


class HostelForm(forms.ModelForm):
    class Meta:
        model  = Hostel
        fields = [
            'sch', 'name', 'code', 'hostel_type', 'category', 'campus',
            'address', 'contact', 'email', 'capacity',
            'warden', 'warden_mobile', 'status', 'description',
        ]
        widgets = {
            'sch':         forms.HiddenInput(),
            'address':     forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BlockForm(forms.ModelForm):
    class Meta:
        model  = Block
        fields = ['hostel', 'name', 'capacity', 'floors', 'warden', 'status']
        widgets = {'hostel': forms.HiddenInput()}

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['hostel'].queryset = Hostel.objects.filter(sch=sch)


class FloorForm(forms.ModelForm):
    class Meta:
        model  = Floor
        fields = ['block', 'floor_number', 'floor_name', 'total_rooms', 'capacity']
        widgets = {'block': forms.HiddenInput()}


class RoomForm(forms.ModelForm):
    class Meta:
        model  = Room
        fields = ['block', 'floor', 'room_number', 'room_type', 'capacity', 'status']
        widgets = {'block': forms.HiddenInput()}

    def __init__(self, *args, block=None, **kwargs):
        super().__init__(*args, **kwargs)
        if block:
            self.fields['floor'].queryset = Floor.objects.filter(block=block)


class BedForm(forms.ModelForm):
    class Meta:
        model  = Bed
        fields = ['room', 'bed_number', 'status']
        widgets = {'room': forms.HiddenInput()}


class HostelAdmissionForm(forms.ModelForm):
    class Meta:
        model  = HostelAdmission
        fields = [
            'sch', 'student', 'hostel', 'block', 'floor', 'room', 'bed',
            'admission_date', 'ac_year', 'emergency_contact',
            'parent_contact', 'medical_notes', 'status', 'remarks',
        ]
        widgets = {
            'sch':            forms.HiddenInput(),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_notes':  forms.Textarea(attrs={'rows': 3}),
            'remarks':        forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset = students.objects.filter(
                school_student=sch, student_status='active'
            ).order_by('first_name')
            self.fields['hostel'].queryset  = Hostel.objects.filter(sch=sch, status='Active')
            self.fields['ac_year'].queryset = academicyr.objects.filter(school_name=sch)
            self.fields['block'].queryset   = Block.objects.filter(hostel__sch=sch)
            self.fields['floor'].queryset   = Floor.objects.filter(block__hostel__sch=sch)
            self.fields['room'].queryset    = Room.objects.filter(block__hostel__sch=sch)
            self.fields['bed'].queryset     = Bed.objects.filter(
                room__block__hostel__sch=sch, status='Available'
            )


class RoomTransferForm(forms.ModelForm):
    class Meta:
        model  = RoomTransfer
        fields = ['sch', 'student', 'from_bed', 'to_bed', 'transfer_date', 'reason']
        widgets = {
            'sch':           forms.HiddenInput(),
            'transfer_date': forms.DateInput(attrs={'type': 'date'}),
            'reason':        forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset  = students.objects.filter(school_student=sch, student_status='active')
            self.fields['from_bed'].queryset = Bed.objects.filter(room__block__hostel__sch=sch, status='Occupied')
            self.fields['to_bed'].queryset   = Bed.objects.filter(room__block__hostel__sch=sch, status='Available')


class WaitingListForm(forms.ModelForm):
    class Meta:
        model  = WaitingList
        fields = ['sch', 'student', 'hostel', 'room_type', 'priority', 'status', 'requested_date', 'remarks']
        widgets = {
            'sch':            forms.HiddenInput(),
            'requested_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks':        forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset = students.objects.filter(school_student=sch, student_status='active')
            self.fields['hostel'].queryset  = Hostel.objects.filter(sch=sch, status='Active')


class HostelFeeTypeForm(forms.ModelForm):
    class Meta:
        model  = HostelFeeType
        fields = ['sch', 'hostel', 'name', 'amount', 'fee_period', 'is_active']
        widgets = {'sch': forms.HiddenInput()}

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['hostel'].queryset = Hostel.objects.filter(sch=sch, status='Active')


class HostelFeeInvoiceForm(forms.ModelForm):
    class Meta:
        model  = HostelFeeInvoice
        fields = [
            'sch', 'student', 'admission', 'fee_type', 'amount', 'discount',
            'issued_date', 'due_date', 'ac_year', 'status',
        ]
        widgets = {
            'sch':         forms.HiddenInput(),
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date':    forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset   = students.objects.filter(school_student=sch, student_status='active')
            self.fields['admission'].queryset = HostelAdmission.objects.filter(sch=sch, status='Active')
            self.fields['fee_type'].queryset  = HostelFeeType.objects.filter(sch=sch, is_active=True)
            self.fields['ac_year'].queryset   = academicyr.objects.filter(school_name=sch)


class HostelFeeReceiptForm(forms.ModelForm):
    class Meta:
        model  = HostelFeeReceipt
        fields = ['invoice', 'receipt_no', 'receipt_date', 'payment_mode', 'amount_paid', 'note']
        widgets = {
            'invoice':      forms.HiddenInput(),
            'receipt_date': forms.DateInput(attrs={'type': 'date'}),
        }


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model  = LeaveApplication
        fields = [
            'sch', 'student', 'hostel', 'from_date', 'to_date',
            'reason', 'destination', 'contact_away', 'parent_notified',
        ]
        widgets = {
            'sch':       forms.HiddenInput(),
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date':   forms.DateInput(attrs={'type': 'date'}),
            'reason':    forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset = students.objects.filter(school_student=sch, student_status='active')
            self.fields['hostel'].queryset  = Hostel.objects.filter(sch=sch, status='Active')


class GatePassForm(forms.ModelForm):
    class Meta:
        model  = GatePass
        fields = [
            'sch', 'student', 'hostel', 'pass_number',
            'out_datetime', 'expected_return', 'purpose',
        ]
        widgets = {
            'sch':             forms.HiddenInput(),
            'out_datetime':    forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'expected_return': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, sch=None, **kwargs):
        super().__init__(*args, **kwargs)
        if sch:
            self.fields['student'].queryset = students.objects.filter(school_student=sch, student_status='active')
            self.fields['hostel'].queryset  = Hostel.objects.filter(sch=sch, status='Active')
