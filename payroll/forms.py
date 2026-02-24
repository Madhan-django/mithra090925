from django import forms
from django.forms import inlineformset_factory
from .models import Department,Designation,PayrollEmployee,PayrollBank,Allowance,Deduction,Loan,Holiday,PayrollSettings,StatutorySettings
emp_type_choice = [
    (1,'PF-ESI'),
    (0,'NON-PF&ESI')
]


class add_deptform(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'sch':forms.HiddenInput()

        }

class add_holidayform(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'sch':forms.HiddenInput()

        }


class add_desgform(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'

class PayrollEmployeeForm(forms.ModelForm):
    class Meta:
        model = PayrollEmployee
        fields = '__all__'
        widgets = {
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'emp_type' : forms.Select(choices=emp_type_choice)
        }

class PayrollBankForm(forms.ModelForm):
    class Meta:
        model = PayrollBank
        fields = '__all__'

PayrollBankFormSet = inlineformset_factory(PayrollEmployee, PayrollBank,fields='__all__', extra=1)
payrollBankFormupdate = inlineformset_factory(PayrollEmployee, PayrollBank,fields='__all__', extra=0)

class Allowanceform(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = '__all__'

class Deductionform(forms.ModelForm):
    class Meta:
        model = Deduction
        fields ='__all__'


class NewLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widget ={
            'end_date':forms.HiddenInput()
        }

from django import forms
from .models import PayrollSettings


class PayrollSettingsForm(forms.ModelForm):

    class Meta:
        model = PayrollSettings
        exclude = ['school', 'created_at']  # we attach school in view

        widgets = {
            "payroll_date": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 31
            }),

            "payroll_month_cycle": forms.Select(attrs={
                "class": "form-select"
            }),

            "total_cl": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

            "cl_per_month": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

            "allow_previous_cl_usage": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "total_ml": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

            "grace_late_count": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

            "lop_after_grace": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.25",
                "min": 0
            }),

            "late_cutoff_hour": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "max": 23
            }),

            "permission_hours": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.25",
                "min": 0
            }),

            "permission_per_month": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),
        }

    # ✅ Validate payroll date
    def clean_payroll_date(self):
        date = self.cleaned_data.get("payroll_date")
        if date and (date < 1 or date > 31):
            raise forms.ValidationError("Payroll date must be between 1 and 31.")
        return date

    # ✅ Business Rule Validation
    def clean(self):
        cleaned_data = super().clean()

        total_cl = cleaned_data.get("total_cl")
        cl_per_month = cleaned_data.get("cl_per_month")

        if total_cl is not None and cl_per_month is not None:
            if cl_per_month > total_cl:
                self.add_error(
                    "cl_per_month",
                    "CL per month cannot be greater than Total CL."
                )

        return cleaned_data

class StatutorySettingsForm(forms.ModelForm):
    class Meta:
        model = StatutorySettings
        exclude = ['sch', 'created_at']
        widgets = {
            'pf_employee_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'pf_employer_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'pf_basic_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'esi_employee_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'esi_employer_percent': forms.NumberInput(attrs={'class': 'form-control'}),
            'esi_gross_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }