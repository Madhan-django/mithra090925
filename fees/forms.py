from django import forms
from .models import fees,addindfee,bulkfee,fee_reciept


isact = [
        ('yes', 'YES'),
    ('no','NO')

    ]
ptype= [
    ('Cash','Cash'),
    ('Cheque','Cheque'),
    ('Net-Banking','Net-Banking'),
    ('Bank-Transfer','Bank-Transfer'),
    ('Demand-Draft','Demand-Draft'),
    ('UPI','UPI')

]
class fee_addform(forms.ModelForm):
    class Meta:
        model = fees
        fields = '__all__'
        widgets = {
            'invoice_title':forms.TextInput(attrs={'class':'form-control','placeholder':'Invoice Title','id':'InvoiceTitle' }),
            'desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Invoice Description'}),
            'issued_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'due_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'fees_school':forms.HiddenInput(),
            'ac_year': forms.HiddenInput(),
            'invoice_no': forms.HiddenInput(),
            'fee_amount':forms.NumberInput(attrs={'class':'form-control','placeholder':'Fee Amount'}),
            'latefee': forms.NumberInput(attrs={'class':'form-control','placeholder':'late Fee'}),
            'isactive': forms.Select(choices=isact,attrs={'class':'form-control'})
        }

class addindfeeform(forms.ModelForm):
    class Meta:
        model = addindfee
        fields = ('fee_cat','class_name','stud_name','concession','status','invoice_no','due_amt',)
        widgets = {

            'fee_cat': forms.Select(attrs={'class': 'form-control'}),
            'class_name': forms.Select(attrs={'class':'form-control'}),
            'status': forms.HiddenInput(),
            'due_amt':forms.HiddenInput(),
            'invoice_no' : forms.HiddenInput(),
            'stud_name':forms.Select(attrs={'class': 'form-control'}),
            'concession':forms.TextInput(attrs={'class': 'form-control'})

        }


class addbulkfeeform(forms.ModelForm):
    class Meta:
       model = bulkfee
       fields ='__all__'

       labels = {

           'fee_cat': 'Fee Category',
           'Class_name': 'Class'
       }

class addfeerecieptform(forms.ModelForm):
    class Meta:
        model = fee_reciept
        fields = '__all__'
        widgets = {
            'payment_type':forms.Select(choices=ptype,attrs={'class':'form-control'}),
            'total':forms.NumberInput(attrs={'readonly':'readonly','class':'form-control'}),
            'reciept_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'paid_amt':forms.NumberInput(attrs={'class':'form-control'}),
            'reciept_no':forms.HiddenInput(),
            'note':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'payment_id':forms.TextInput(attrs={'class':'form-control'}),
            'reciept_inv':forms.HiddenInput()


        }