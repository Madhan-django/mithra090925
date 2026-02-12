from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Category, Supplier,Order,product_set,stock,products,Purchase,book_set_issue,ind_book,group_set
from .forms import (
    CategoryForm,
    SupplierForm,
    PurchaseForm,
    OrderForm,
    book_set_issue_form,
    ProductSetForm,
    stockForm,
    ProductForm,
    ind_bookForm,
    group_set_form,
    UpdatePurchaseForm
)
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,section
from authenticate.decorators import allowed_users
from django.contrib import messages
from admission.models import students
from django.core.paginator import Paginator
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
    return render(request, 'inventory/category_list.html', {'data': categories,'skool':sdata,'year':year})

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

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def supplier_update(request, pk):
    # Fetch school info from session
    sch_id = request.session.get('sch_id')
    if not sch_id:
        messages.error(request, "Session expired or invalid. Please log in again.")
        return redirect('login')

    sdata = get_object_or_404(school, pk=sch_id)

    # Get academic year details safely
    try:
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (currentacademicyr.DoesNotExist, academicyr.DoesNotExist):
        messages.warning(request, "Academic year data is missing for this school.")
        year = None

    # Get supplier record
    supplier = get_object_or_404(Supplier, pk=pk)

    # Handle form submission
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier details updated successfully.')
            return redirect('supplier_list')

    form = SupplierForm(instance=supplier)

    # Render template
    return render(request, 'inventory/supplier_update.html', {
        'form': form,
        'skool': sdata,
        'year': year
    })


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
    cty = Category.objects.filter(Cat_school=sdata)
    supl = Supplier.objects.filter(Sup_school=sdata)
    prods = products.objects.filter(sch=sdata)
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
            return redirect('purchase_list')
    else:
        form = PurchaseForm(initial=initial_data)
        form.fields['name'].queryset=prods
        form.fields['category'].queryset=cty
        form.fields['supplier'].queryset= supl
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
            return redirect('products_list')

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
            print("0------------invalid")
    else:
        form = ProductSetForm(initial=initial_data)
        form.fields['prod_set']=prod

    return render(request, 'inventory/product_set_create.html', {'form': form,'cls':cls,'prod':prod,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_set_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = product_set.objects.filter(prod_set__sch=sdata)
    return render(request, 'inventory/product_set_list.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def product_set_update(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    prod_set = product_set.objects.get(pk=pk)
    cls = sclass.objects.filter(school_name=sdata,acad_year=yr)
    prods = products.objects.filter(sch=sdata)
    if request.method == 'POST':
        form = ProductSetForm(request.POST, instance=prod_set)
        if form.is_valid():
            form.save()
            return redirect('product_set_list')
    else:
        form = ProductSetForm(instance=prod_set)
        form.fields['pclass'].queryset=cls
        form.fields['prod_set'].queryset= prods
    return render(request, 'inventory/product_set_update.html', {'form': form, 'prod_set': prod_set,'cls':cls,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def product_set_delete(request, pk):
    prod_set = product_set.objects.get(id=pk)
    prod_set.delete()
    messages.success(request,"Product Deleted Successfully")
    return redirect('product_set_list')


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
    data = students.objects.filter(school_student=sdata, ac_year=year, student_status='Active')
    initial_data = {
        'set_school':sdata
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
    paginator = Paginator(data, 30)  # Show 30 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object

    return render(request, 'inventory/book_set_issue.html', {'bkset':bkset,'skool':sdata,'year':year,'data': page_obj})

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
    print("ssssssssssssssssssssssssssssssssssssss",data)
    return render(request, 'inventory/purchase.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def purchase_update(request, pur_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Purchase.objects.get(id=pur_id)
    prods = products.objects.filter(sch=sdata)
    cats = Category.objects.filter(Cat_school=sdata)
    supls = Supplier.objects.filter(Sup_school=sdata)

    if request.method == 'POST':
        form = UpdatePurchaseForm(request.POST, instance=data)
        form.fields['name'].queryset = prods
        form.fields['category'].queryset = cats
        form.fields['supplier'].queryset = supls

        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase Updated Successfully')
            return redirect('purchase_list')
        else:
            # If form is invalid → fall through to render again
            messages.error(request, 'Please correct the errors below.')
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",form.errors)
    else:
        form = UpdatePurchaseForm(instance=data)

        form.fields['category'].queryset = cats
        form.fields['supplier'].queryset = supls


    # Always return a response (even when form invalid)
    return render(
        request,
        'inventory/purchase_update.html',
        {'form': form, 'skool': sdata, 'year': year}
    )


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


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def reciept_ind_book(request, stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    # Get current academic year
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # Get student details
    student_id = students.objects.get(pk=stud_id)

    # All stock entries for this school
    stk = stock.objects.filter(Prod_school=sdata)

    # ✅ Corresponding product list
    product_qs = products.objects.filter(stock__Prod_school=sdata).distinct()

    # Pre-fill form defaults
    initial_data = {
        'ind_school': sdata,
        'bclass': student_id.class_name,
        'stud': student_id
    }

    # --- POST ---
    if request.method == 'POST':
        form = ind_bookForm(request.POST)
        form.fields['inv_prod'].queryset = product_qs   # ✅ correct queryset

        if form.is_valid():
            fprod = form.cleaned_data['inv_prod']  # this is a products instance
            quanty = form.cleaned_data['qty']

            print("Selected product:", fprod.name)

            try:
                pro = stk.get(name=fprod)
                if pro.quantity >= quanty:
                    pro.quantity -= quanty
                    pro.save()
                    form.save()
                    messages.success(request, 'Bill Added Successfully')
                    return redirect('reciept_book_set')
                else:
                    messages.error(request, f"Not enough stock for {fprod.name}. Available: {pro.quantity}")
                    return redirect('reciept_ind_book', stud_id=stud_id)
            except stock.DoesNotExist:
                messages.warning(request, f"Product '{fprod.name}' not found in stock list.")
        else:
            print("Form invalid:", form.errors)

    # --- GET ---
    else:
        form = ind_bookForm(initial=initial_data)
        form.fields['inv_prod'].queryset = product_qs   # ✅ correct queryset for dropdown

    return render(
        request,
        'inventory/ind_book_reciept.html',
        {
            'form': form,
            'skool': sdata,
            'year': year,
            'stk': stk
        }
    )


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




@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def book_set_rec(request,stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = students.objects.get(pk=stud_id)
    prod_set = group_set.objects.filter(group_school=sdata,acad_year=year)

    initial_data = {
        'book_student' : data,
        'stud_class':data.class_name,
        'set_school':sdata

    }
    if request.method == 'POST':
        form = book_set_issue_form(request.POST)
        if form.is_valid():
            book_set = form.cleaned_data['book_set']
            grp_set = group_set.objects.get(name=book_set,acad_year=year,group_school=sdata)
            books = product_set.objects.filter(name=grp_set)
            stk = stock.objects.filter(Prod_school=sdata)
            for book in books:
                for prod in stk:
                    if prod.name==book.prod_set:
                        prod.quantity=prod.quantity-book.qty
                        prod.save()

            form.save()
            messages.success(request,"Book Set Issued successfully")
            return redirect('reciept_book_set')
    form = book_set_issue_form(initial=initial_data)
    return render(request, 'inventory/book_set_rec.html', {'form': form,'bkset':prod_set,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def bootset_issued(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data  = book_set_issue.objects.filter(set_school=sdata)
    paginator = Paginator(data, 30)  # Show 30 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    return render(request, 'inventory/book_reciept.html',
                  context={'bkset': page_obj, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def bookset_delete(request,set_id):
    print("ddddddddddddddddddddddddddd",set_id)
    data = book_set_issue.objects.all()
    for dt in data:
        print("sssssssssssssssssssssss",dt,dt.id)


    messages.success(request,"Book Set Deleted Successfully")
    return redirect('bootset_issued')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def group_set_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = group_set.objects.filter(group_school = sdata,acad_year = year)
    return render(request,'inventory/group_list.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def group_set_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'acad_year':year,
        'group_school':sdata
    }

    if request.method=='POST':
        form = group_set_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Group Created Successfully')
            return redirect('group_set_list')
    form = group_set_form(initial=initial_data)
    return render(request,'inventory/group_set_create.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def group_set_update(request, pk):
    # Fetch school info from session
    sch_id = request.session.get('sch_id')
    if not sch_id:
        messages.error(request, "Session expired or invalid. Please log in again.")
        return redirect('login')

    sdata = get_object_or_404(school, pk=sch_id)

    # Get academic year details safely
    try:
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (currentacademicyr.DoesNotExist, academicyr.DoesNotExist):
        messages.warning(request, "Academic year data is missing for this school.")
        year = None

    # Get the group record to update
    group = get_object_or_404(group_set, pk=pk)

    if request.method == 'POST':
        form = group_set_form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group updated successfully.")
            return redirect('group_set_list')

    form = group_set_form(instance=group)

    return render(request, 'inventory/group_set_update.html', {
        'form': form,
        'skool': sdata,
        'year': year,
        'update': True  # optional flag if you want to show "Update" in template
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def group_set_delete(request, pk):
    # Fetch the group record
    group = get_object_or_404(group_set, pk=pk)

    # Optional: Only allow POST for deleting
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group deleted successfully.")
        return redirect('group_set_list')

    # If GET request, redirect to list with warning
    messages.warning(request, "Invalid request to delete group.")
    return redirect('group_set_list')
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def indbook_issued(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data  = ind_book.objects.filter(ind_school=sdata)
    paginator = Paginator(data, 30)  # Show 30 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    return render(request, 'inventory/indbook_reciept.html',
                  context={'bkset': page_obj, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def indbook_delete(request, ind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # Get the issued record
    indbook = get_object_or_404(ind_book, id=ind_id)

    # --- Find category via Purchase ---
    purchase = Purchase.objects.filter(name=indbook.inv_prod).first()
    category = purchase.category if purchase else None

    # --- Update or create stock ---
    try:
        stk = stock.objects.get(name=indbook.inv_prod, Prod_school=sdata)
        stk.quantity += indbook.qty
        stk.save()
    except stock.DoesNotExist:
        stock.objects.create(
            name=indbook.inv_prod,
            description=f"Auto-added on delete of issued product {indbook.inv_prod.name}",
            category=category if category else Category.objects.first(),  # fallback if missing
            quantity=indbook.qty,
            Prod_school=sdata
        )

    # --- Delete the issued book record ---
    indbook.delete()

    messages.success(request, "Issued book deleted and stock updated successfully.")
    return redirect('indbook_issued')  # update with your redirect

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def stud_search(request):
    sch_id = request.session.get('sch_id')
    if not sch_id:
        raise Http404("School ID not found in session")

    sdata = school.objects.get(pk=sch_id)
    curr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=curr, school_name=sdata)

    # default empty queryset
    data = students.objects.none()

    # handle search params
    Searchby = request.GET.get('searchby') or request.POST.get('searchby')
    Searched = request.GET.get('searched') or request.POST.get('searched')

    if Searchby and Searched:
        if Searchby == 'studname':
            data = students.objects.filter(first_name__istartswith=Searched, school_student=sdata)
        elif Searchby == 'fathername':
            data = students.objects.filter(father_name__istartswith=Searched, school_student=sdata)
        elif Searchby == 'studmob':
            data = students.objects.filter(phone__startswith=Searched, school_student=sdata)
        elif Searchby == 'studclass':
            try:
                srh = sclass.objects.get(name=Searched, school_name=sdata, acad_year=year)
                data = students.objects.filter(class_name=srh, school_student=sdata)
            except sclass.DoesNotExist:
                messages.info(request, "No Class Found")
                data = students.objects.none()
        elif Searchby == 'userid':
            data = students.objects.filter(usernm=Searched)
        else:
            data = students.objects.filter(student_status=Searched, school_student=sdata)

    paginator = Paginator(data, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/book_set_issue.html', {
        'data': page_obj,
        'skool': sdata,
        'year': year,
        'searchby': Searchby,
        'searched': Searched,
    })

