from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Category, Supplier,Order,product_set,stock,products,Purchase,book_set_issue,ind_book
from .forms import CategoryForm, SupplierForm, PurchaseForm, OrderForm,book_set_issue_form,ProductSetForm,stockForm,ProductForm,ind_bookForm
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,section
from authenticate.decorators import allowed_users
from django.contrib import messages
from admission.models import students
from django.db.models import Q
from .utils import render_to_pdf
import datetime


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def category_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'Cat_school': sdata
    }
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New Category has been Added Successfully')
            return redirect('category_list')
    else:
        form = CategoryForm(initial=initial_data)
    return render(request,'inventory/category_create.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def category_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    categories = Category.objects.filter(Cat_school=sdata)
    initial_data = {
        'Cat_school': sdata
    }
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Category has been Added Successfully')
            return redirect('category_list')
    form = CategoryForm(initial=initial_data)
    return render(request, 'inventory/category_list.html', {'data': categories,'form':form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def category_update(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Updated Successfully')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'inventory/category_update.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request,'Category Deleted Successfully')
    return redirect('category_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def supplier_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'Sup_school':sdata
    }
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(initial=initial_data)
    return render(request,'inventory/supplier_create.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def supplier_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Supplier.objects.filter(Sup_school=sdata)
    return render(request, 'inventory/supplier_list.html', {'data': data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def supplier_update(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request,'Supplier Contacts updated Successfully')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'inventory/supplier_update.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def purchase_entry(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'Prod_school':sdata
    }
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            pur_name = form.cleaned_data['name']
            qty = form.cleaned_data['quantity']
            desc = form.cleaned_data['description']
            cat = form.cleaned_data['category']
            stk = stock.objects.filter(Prod_school=sdata,name= pur_name).exists()
            if stk:
                stk_add = stock.objects.get(Prod_school=sdata,name= pur_name)
                stk_add.quantity = stk_add.quantity + qty
                stk_add.save()

            else:
                stk_add = stock(name=pur_name,description=desc,category=cat,quantity=qty,Prod_school=sdata)
                stk_add.save()
            form.save()
            return redirect('/')
    else:
        form = PurchaseForm(initial=initial_data)
    return render(request, 'inventory/purchase_entry.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def stock_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    stk = stock.objects.filter(Prod_school=sdata)
    return render(request, 'inventory/stock_list.html', {'data': stk,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_update(request,pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    product = get_object_or_404(products,id = pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_update.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def product_delete(request, pk):
    prod = products.objects.get(pk=pk)
    prod.delete()
    return redirect('products_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_set_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    prod = products.objects.filter(sch=sdata)
    initial_data = {
        'ac_year':year
    }
    if request.method == 'POST':
        form = ProductSetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_set_list')
    else:
        form = ProductSetForm(initial=initial_data)
    return render(request, 'inventory/product_set_create.html', {'form': form,'cls':cls,'prod':prod,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_set_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = product_set.objects.filter(prod_set__Prod_school=sdata)
    return render(request, 'inventory/product_set_list.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_set_update(request, pk):
    prod_set = get_object_or_404(product_set, pk=pk)
    if request.method == 'POST':
        form = ProductSetForm(request.POST, instance=prod_set)
        if form.is_valid():
            form.save()
            return redirect('your_app_name:product_set_list')
    else:
        form = ProductSetForm(instance=prod_set)
    return render(request, 'your_app_name/product_set_update.html', {'form': form, 'prod_set': prod_set})

@allowed_users(allowed_roles=['superadmin','Admin'])
def product_set_delete(request, pk):
    prod_set = get_object_or_404(product_set, pk=pk)
    if request.method == 'POST':
        prod_set.delete()
        return redirect('product_set_list')
    return render(request, 'inventory/product_set_delete.html', {'prod_set': prod_set})

def load_class_prod(request):
    print('########## in func')
    selclass = request.GET.get('selclassid')
    data = students.objects.filter(class_name=selclass)
    return render(request, 'fee/students_dropdown_list_options.html', {'data': data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def reciept_book_set(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'set_school':sdata
    }
    initial_data1 = {
        'ind_school': sdata
    }
    bkset = book_set_issue.objects.filter(set_school=sdata)
    if request.method == 'POST':
        form = book_set_issue_form(request.POST)
        if form.is_valid():
            cls = form.cleaned_data['stud_class']
            data = product_set.objects.filter(pclass=cls)
            prod_sch = stock.objects.filter(Prod_school=sdata)
            for prod in data:
                for totprod in prod_sch:
                    if prod.prod_set.name == totprod.name:
                        totprod.quantity = totprod.quantity-prod.qty
                        totprod.save()
            form.save()
            messages.success(request,'Book Set Record Added Successfully')
        return redirect('reciept_book_set')
    else:
        form = book_set_issue_form(initial=initial_data)

    return render(request, 'inventory/book_set_issue.html', {'form': form,'bkset':bkset,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'sch':sdata
    }
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(initial=initial_data)
    return render(request, 'inventory/product_create.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def products_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = products.objects.filter(sch=sdata)
    initial_data={
        'sch':sdata
    }
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    form = ProductForm(initial=initial_data)
    return render(request,'inventory/products.html',context={'data':data,'skool':sdata,'year':year,'form':form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def purchase_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Purchase.objects.filter(Prod_school=sdata)
    return render(request, 'inventory/purchase.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def purchase_update(request,pur_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Purchase.objects.get(id=pur_id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Purchase Added Successfully')
            return redirect('purchase_list')
    else:
        form = PurchaseForm(instance=data)
        return render(request,'inventory/purchase_update.html',context={'form':form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin'])
def purchase_delete(request,pur_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Purchase.objects.get(id=pur_id)
    data.delete()
    messages.success(request,'Purchase Entry Deleted Successfully')
    return redirect('purchase_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def reciept_ind_book(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    ind_bk = ind_book.objects.filter(ind_school=sdata)
    initial_data = {
        'ind_school':sdata
    }
    stk = stock.objects.filter(Prod_school=sdata)
    if request.method == 'POST':
        form = ind_bookForm(request.POST)
        if form.is_valid():
            fprod = form.cleaned_data['inv_prod']
            quanty = form.cleaned_data['qty']

            for pro in stk:
                if fprod == pro.name:

                    pro.quantity = pro.quantity-quanty
                    pro.save()
            form.save()
            messages.success(request,'Bill Added Successfully')
            return redirect('reciept_book_set')
        else:
            print('form invalid')
    form = ind_bookForm(initial=initial_data)
    return render(request,'inventory/ind_book_reciept.html',context={'form':form,'skool':sdata,'year':year,'ind_bk':ind_bk})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def set_search_view(request):
   date1 = request.POST.get('start_date')
   date2 = request.POST.get('end_date')
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   initial_data = {
       'set_school':sdata
   }
   filtered_data = book_set_issue.objects.filter(
       Q(issue_date__range=[date1, date2]) &
       Q(set_school=sdata)
   )
   form = book_set_issue_form(initial=initial_data)
   return render(request, 'inventory/book_set_issue.html', {'form': form, 'bkset': filtered_data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def book_set_pdf(request):
    date1 = request.POST.get('start_date')
    date2 = request.POST.get('end_date')
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    current_datetime = datetime.datetime.now()
    filtered_data = book_set_issue.objects.filter(
        Q(issue_date__range=[date1, date2]) &
        Q(set_school=sdata)
    )
    data= {
        'filtered_data':filtered_data,
        'skool': sdata,
        'year': year,
        'dt_tm': current_datetime,
    }
    pdf = render_to_pdf('inventory/generate_pdf.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def ind_search_view(request):
   date1 = request.POST.get('start_date')
   date2 = request.POST.get('end_date')
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   initial_data = {
       'ind_school':sdata
   }
   filtered_data = ind_book.objects.filter(
       Q(issue_date__range=[date1, date2]) &
       Q(set_school=sdata)
   )
   form = ind_bookForm(initial=initial_data)
   return render(request, 'inventory/book_set_issue.html', {'form': form, 'ind_bk': filtered_data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def ind_book_pdf(request):
    date1 = request.POST.get('start_date')
    date2 = request.POST.get('end_date')
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    current_datetime = datetime.datetime.now()
    filtered_data = ind_book.objects.filter(
        Q(issue_date__range=[date1, date2]) &
        Q(ind_school=sdata)
    )
    data= {
        'filtered_data':filtered_data,
        'skool': sdata,
        'year': year,
        'dt_tm': current_datetime,
    }
    pdf = render_to_pdf('inventory/ind_book_pdf.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def stock_gen_pdf(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    stk = stock.objects.filter(Prod_school=sdata)
    current_datetime = datetime.datetime.now()
    data = {
        'stk': stk,
        'skool':sdata,
        'year':year,
        'dt_tm':current_datetime,
    }
    pdf = render_to_pdf('inventory/stock_gen_pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def load_section(request):
    class_id = request.GET.get('Class_Id')
    sstudents = students.objects.filter(class_name=class_id).order_by('first_name')
    return render(request, 'inventory/selectstudent.html',context={'ssection': sstudents})