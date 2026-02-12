from django import forms
from django.forms import inlineformset_factory
from .models import Department,Designation,PayrollEmployee,PayrollBank,Allowance,Deduction,Loan
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