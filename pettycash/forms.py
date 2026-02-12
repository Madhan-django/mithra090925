from django import forms
from .models import CashSource,PettyCashExpense,ExpenseCategory

class NewCashSourceForm(forms.ModelForm):
    class Meta:
        model= CashSource
        fields = '__all__'
        widgets = {
            'source_name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control'}),
            'date_received': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'received_by':forms.HiddenInput(),
            'source_school':forms.HiddenInput(),
            'school_year':forms.HiddenInput()
        }

from django import forms
from django.contrib.auth.models import User
from .models import PettyCashExpense

class NewPettyCashExpenseForm(forms.ModelForm):
    class Meta:
        model = PettyCashExpense
        fields = '__all__'
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_spent': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'spent_by': forms.TextInput(attrs={'class': 'form-control'}),
            'approved_by': forms.HiddenInput(),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'petty_school': forms.HiddenInput(),
            'school_year':forms.HiddenInput(),
            'balance':forms.HiddenInput(),
            'expense_no':forms.HiddenInput()
        }




class NewExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields= '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'expense_school':forms.HiddenInput()
        }