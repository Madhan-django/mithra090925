from django import forms
from .models import Category, Supplier,stock, Order,product_set,book_set_issue,Purchase,products,ind_book,group_set
from django.forms import formset_factory

sts = (
    ('Issued','Issued'),
    ('Not-Issued','Not-Issued'),
    ('Pending','pending')
)

bk_set = (
    ('No','No'),
    ('YES','YES'),

)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','Cat_school')
        
        labels ={
              'name':'Category Name'


}
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'Cat_school':forms.HiddenInput()
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        labels = {
        'name' : 'Company Name',
        'contact_person':'Contact Person',
        'email':'Email',
        'address' : 'Address',
        'contact_number' :'Contact No',
        'contact_number2':'Alternate No'

        }

        widgets = {
            'Sup_school':forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'contact_person': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'contact_number': forms.TextInput(attrs={'class':'form-control'}),
             'contact_number2':forms.TextInput(attrs={'class':'form-control'}),
        }


class stockForm(forms.ModelForm):
    class Meta:
        model = stock
        fields = ('name', 'description', 'category','quantity','Prod_school')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'quantity')

class group_set_form(forms.ModelForm):
    class Meta:
        model = group_set
        fields = '__all__'
       
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'acad_year':forms.HiddenInput(),
            'group_school':forms.HiddenInput()
        }

class ProductSetForm(forms.ModelForm):
    class Meta:
        model = product_set
        fields = '__all__'
        labels = {

             'pclass':'Class',
             'prod_set': 'Product',
             'qty':'Quantity'
         }

        widgets= {
            'name':forms.Select(attrs={'class':'form-control'}),
            'ac_year': forms.HiddenInput(),
            'pclass':forms.Select(attrs={'class':'form-control'}),
            'prod_set':forms.Select(attrs={'class':'form-control'}),
            'qty': forms.NumberInput(attrs={'class':'form-control'}),

        }


class book_set_issue_form(forms.ModelForm):
    class Meta:
        model = book_set_issue
        fields = '__all__'

        widgets = {
            'status':forms.Select(choices=sts,attrs={'class':'form-control'}),
            'set_school':forms.HiddenInput(),
            'book_set': forms.Select(attrs={'class':'form-control'}),
            'issue_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'stud_class': forms.HiddenInput(),
            'book_student': forms.HiddenInput()
        }
        labels = {
            'set_school':'School',
            'book_set': 'Book Set',
            'issue_date':'Date',
            'stud_class':'Class',
            'book_student':'Sudent Name',


        }



class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

        labels = {
            'name': 'Product',
            'description': 'Description',
            'category': 'Category',
            'supplier': 'Supplier',
            'price': 'Price',
            'quantity': 'Quantity',
            'invoice_no': 'Invoice No',
            'order_dt': 'Ordered Date',
            'rec_dt': 'Received Date',
        }

        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rec_dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Prod_school': forms.HiddenInput(),
        }

class UpdatePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

        labels = {
            'name': 'Product',
            'description': 'Description',
            'category': 'Category',
            'supplier': 'Supplier',
            'price': 'Price',
            'quantity': 'Quantity',
            'invoice_no': 'Invoice No',
            'order_dt': 'Ordered Date',
            'rec_dt': 'Received Date',
        }

        widgets = {
            'name': forms.HiddenInput(),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rec_dt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Prod_school': forms.HiddenInput(),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = '__all__'

        labels ={
            'name': 'Product Name',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'sch':forms.HiddenInput()
        }

class ind_bookForm(forms.ModelForm):
    class Meta:
        model = ind_book
        fields = '__all__'

        widgets = {
            'isbook_set':forms.Select(choices=bk_set,attrs={'class':'form-control'}),
            'inv_prod': forms.Select(attrs={'class':'form-control'}),
            'issue_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'stud': forms.HiddenInput(),
            'bclass':forms.HiddenInput(),
            'qty':forms.NumberInput(attrs={'class':'form-control'}),
            'status':forms.Select(choices=sts,attrs={'class':'form-control'}),
            'ind_school':forms.HiddenInput()

        }
        labels = {
            'isbook_set':'Book Set',
            'inv_prod':'Product',
            'issue_date':'Date',
            'stud': 'Student',
            'bclass': 'Class',
            'qty': 'Quantity',
            'status': 'Status',


        }


