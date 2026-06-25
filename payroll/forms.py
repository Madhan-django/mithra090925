from django import forms
from django.forms import inlineformset_factory
from .models import Department,PayrollEmployee,PayrollBank,Allowance,Loan,Holiday,PayrollSettings,StatutorySettings,Deductions,staff_deduction,PayrollSettings

emp_type_choice = [
    (1,'PF-ESI'),
    (0,'NON-PF&ESI')
]

sts = [
    ('Active','Active'),
    ('Inactive','Inactive')
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
        labels = {
            'name':'Holiday Category',

        }
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'sch':forms.HiddenInput(),


        }



class PayrollEmployeeForm(forms.ModelForm):
    class Meta:
        model = PayrollEmployee
        fields = [
            "gross_salary",
            "basic_percentage",
            "hra_percentage",
            "wages_per_day",
        ]


class Allowanceform(forms.ModelForm):
    class Meta:
        model = Allowance
        fields = '__all__'

class Deductionform(forms.ModelForm):
    class Meta:
        model = Deductions
        fields ='__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'sch': forms.HiddenInput()
        }

class staff_Deductionform(forms.ModelForm):
    class Meta:
        model = staff_deduction
        fields ='__all__'
        widgets={
            'name' :forms.Select(attrs={'class':'form-control'}),
            'staff' : forms.Select(attrs={'class':'form-control'}),
            'ded_amount' : forms.NumberInput(attrs={'class':'form-control'}),
            'start_date' : forms.DateInput(attrs={'class':'form-control','type': 'date'}),
            'end_date' : forms.DateInput(attrs={'class':'form-control','type': 'date'}),
            'active' : forms.Select(choices=sts,attrs={'class':'form-control'}),
            'sch' : forms.HiddenInput()
        }



class NewLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widget ={
            'end_date':forms.HiddenInput()
        }




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

            "Sandwich_Leave_Policy": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "half_day_as_cl": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "grace_late_count": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),
            "grace_mins": forms.NumberInput(attrs={
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

class PayrollBankForm(forms.ModelForm):
    class Meta:
        model = PayrollBank
        fields= '__all__'

        widgets = {

            'CustName': forms.Select(attrs={
                'class': 'form-control select2'
            }),

            'home_school': forms.Select(attrs={
                'class': 'form-control'
            }),

            'AccNo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Account Number'
            }),

            'CIFNo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CIF Number (Optional)'
            }),

            'BankName': forms.Select(attrs={
                'class': 'form-control select2'
            }),

            'Branch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Branch Name'
            }),

            'IFSC': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter IFSC Code'
            }),
        }