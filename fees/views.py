from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator
from django.db.models import Sum
from .models import fees,addindfee,fee_reciept
from admission.models import students
from .forms import fee_addform,addindfeeform,addbulkfeeform,addfeerecieptform,updateindfeeform,updateindfee_catform
from django.contrib import messages
from institutions.models import school
from authenticate.decorators import allowed_users
from setup.models import currentacademicyr,sclass,section,academicyr,receipt_template
from num2words import num2words
import time
import datetime
import os
from django.http import HttpResponse
from django.views.generic import View

from .utils import render_to_pdf

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def fee_details(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr,school_name=sdata)
    data = fees.objects.filter(fees_school=sdata,ac_year=year)
    paginator = Paginator(data, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'fee/fee_list.html',context={'data':page_obj,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def fee_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    cdata = sclass.objects.filter(school_name=sdata).values()
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr,school_name=sdata)
    yr2 = academicyr.objects.filter(school_name=sdata)
    inv = fees.objects.filter(fees_school=sch_id).count() + 1
    initial_data = {
        'fees_school': sdata,
        'ac_year':year,
        'invoice_no': inv
    }
    if request.method == 'POST':
        form = fee_addform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Record has been added successfully!')
            return redirect('fee_details')
    else:
        form = fee_addform(initial=initial_data)
    return render(request,'fee/addfee.html',context={'form':form,'options':cdata,'skool':sdata,'year':year,'yr2':yr2})




@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addfeeind(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr,school_name=sdata)
    data = fees.objects.filter( fees_school=sch_id,ac_year=year)
    cdata = sclass.objects.filter(school_name=sch_id)
    years = academicyr.objects.filter(school_name=sdata)
    initial_data = {
        'status':'Unpaid',
        'invoice_no': 0,
        'due_amt':0,
    }
    if request.method == 'POST':
        form = addindfeeform(request.POST)
        if form.is_valid():
            fee_ct = form.cleaned_data['fee_cat']
            tmp = form.save(commit=False)
            tmp.due_amt = fee_ct.fee_amount
            tmp.invoice_no = addindfee.objects.filter(fee_cat__fees_school=sch_id).count() + 1
            tmp.save()
            return redirect('invoices')
        else:
            messages.success(request,'invalid form data')
            return redirect('addindfee')

    form= addindfeeform(initial=initial_data)
    form1 = addbulkfeeform()
    return render(request,'fee/addindfee.html',context={'form':form,'data':data,'cdata':cdata,'skool':sdata,'form1':form1,'years':years})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def fee_invoices(request):
    sch_id = request.session['sch_id']
    sdata= school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.filter(fee_cat__fees_school=sdata,fee_cat__ac_year=year)
    paginator = Paginator(data,30)
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)
    return render(request, 'fee/fee_details.html', context={'data': page_obj,'skool':sdata})
    
def fee_invoices_del(request):
    sch_id = request.session['sch_id']
    sdata= school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.filter(fee_cat__fees_school=sdata,fee_cat__ac_year=year)
    data.delete()
    return HttpResponse("Invoice deleted")    

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addbulkfee(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr,school_name=sdata)
    data = fees.objects.filter(fees_school=sch_id, ac_year=year)
    if request.method == 'POST':
        form = addbulkfeeform(request.POST)
        if form.is_valid():
            fee_cat = form.cleaned_data['fee_cat']
            fee_class = form.cleaned_data['class_name']
            years = form.cleaned_data['years']
            stud = students.objects.filter(school_student=sch_id,class_name=fee_class,ac_year=years)
            print('stud',stud)
            inv_no = addindfee.objects.filter(fee_cat__fees_school=sch_id).count()
            for student in stud:
                inv_no = inv_no + 1
                
                addindfee.objects.create(fee_cat=fee_cat,class_name=fee_cat.iclass,stud_name=student,concession=0,status='Unpaid',invoice_no=inv_no,due_amt=fee_cat.fee_amount)
        messages.success(request, 'Fee has been Generated Successfully.')
        return redirect('invoices')
    form = addbulkfeeform()
    return render(request,'fee/bulkfee.html',context={'form':form,'skool':sdata,'data':data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updatefee_cat(request,fee_cat_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data =fees.objects.get(pk=fee_cat_id)
    iclass = sclass.objects.filter(school_name=sdata)
    yr2 = academicyr.objects.filter(school_name=sdata)
    if request.method == 'POST':
        form =fee_addform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Updated Successfully')
            return redirect('fee_details')
    else:
        form = fee_addform(instance=data)
    return render(request, 'fee/updatefee.html',context={'form': form,'skool':sdata,'iclass':iclass,'yr2':yr2})



@allowed_users(allowed_roles=['superadmin','Admin'])
def delfee_cat(request,fee_cat_id):
    data = fees.objects.get(pk=fee_cat_id)
    data.delete()
    messages.success(request,'Record Deleted successfully')
    time.sleep(5)
    return redirect('fee_details')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updateindfee(request,feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = addindfee.objects.get(pk=feeind_id)
    form = updateindfeeform(request.POST or None,instance=data)

    if form.is_valid():
        form.save()
        messages.success(request, 'Record Updated Successfully')
        return redirect('invoices')
    return render(request,'fee/updateindfee.html',context={'form':form,'skool':sdata})


@allowed_users(allowed_roles=['superadmin','Admin'])
def delindfee(request,feeind_id):
    data = addindfee.objects.get(pk=feeind_id)
    data.delete()
    messages.success(request, 'Record Deleted Successfully')
    return redirect('invoices')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addfeereciept(request,feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    recindfee = addindfee.objects.get(pk=feeind_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    if recindfee.status=='Paid':
        messages.success(request,'Fees Already paid')
        return redirect('invoices')
    else:
        if not recindfee.concession_apply :
            recindfee.due_amt= recindfee.due_amt-recindfee.concession
            recindfee.concession_apply = True
        rec_no = fee_reciept.objects.all().count() + 1
        initial_data = {
            'reciept_inv': recindfee,
            'total': recindfee.due_amt,
            'paid_amt':recindfee.due_amt,
            'reciept_no':rec_no
        }
        if request.method == 'POST':
            try:
                form = addfeerecieptform(request.POST)
                if form.is_valid():
                    tot1 = form.cleaned_data.get("total")
                    paid_amt1 = form.cleaned_data.get("paid_amt")
                    if paid_amt1 == tot1:
                        recindfee.status = 'Paid'
                        recindfee.due_amt = 0
                        recindfee.save(update_fields=["status", "due_amt","concession_apply"])
                        new_record = form.save()

                        rec_data = fee_reciept.objects.get(id=new_record.id)
                        try:
                            rec = receipt_template.objects.get(school_name=sdata)
                            rec_temp = rec.template
                        except receipt_template.DoesNotExist:
                            rec_temp = 'fee/reciept_show.html'
                        amt_words = num2words(paid_amt1, lang='en_IN').title()
                        return render(request,rec_temp, context={'data': rec_data, 'sch_name': sdata,'skoollogo':skoollogo,'amt_words':amt_words})
                    elif paid_amt1 < tot1:
                        recindfee.status = 'Partially Paid'
                        recindfee.due_amt = recindfee.due_amt - paid_amt1
                        recindfee.save(update_fields=["status", "due_amt","concession_apply"])
                        new_record = form.save()
                        messages.success(request, 'Fee Paid Successfully')
                        rec_data = fee_reciept.objects.get(id=new_record.id)
                        try:
                            rec = receipt_template.objects.get(school_name=sdata)
                            rec_temp = rec.template
                        except receipt_template.DoesNotExist:
                            rec_temp = 'fee/reciept_show.html'
                        amt_words = num2words(paid_amt1, lang='en_IN').title()
                        return render(request, rec_temp, context={'data': rec_data, 'sch_name': sdata,'skoollogo':skoollogo,'amt_words':amt_words})
                    else:
                        messages.warning(request, 'Invalid Amount')
                        redirect('invoices')
            except Exception as e:
                error_message = str(e)
                return HttpResponse(f"Error: {error_message}", status=500)
        
    form = addfeerecieptform(initial=initial_data)
    return render(request,'fee/addfeereciept.html',context={'form':form,'recindfee':recindfee,'skool':sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def fee_reciepts(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = fee_reciept.objects.filter(reciept_inv__fee_cat__ac_year=year)
    paginator = Paginator(data, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'fee/fee_reciepts.html',context={'data':page_obj,'skool':sdata,'year':year})

def load_class(request):
    selclass = request.GET.get('selclassid')
    data = students.objects.filter(class_name=selclass)
    return render(request, 'fee/students_dropdown_list_options.html', {'data': data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def html_to_pdf_directly(request,ret_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = fee_reciept.objects.get(pk=ret_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    data = {
        'sch_name':sdata,
        'rec_no':rec_data.reciept_no,
        'rec_date':rec_data.reciept_date,
        'rec_stud':rec_data.reciept_inv.stud_name,
        'rec_inv':rec_data.reciept_inv.fee_cat,
        'rec_total':rec_data.total,
        'rec_paid_amt':rec_data.paid_amt,
        'rec_ptype':rec_data.payment_type,
        'sch_addr':sdata.address,
        'rec_mob':rec_data.reciept_inv.stud_name.phone,
        'rec_admn': rec_data.reciept_inv.stud_name.admn_no,
        'rec_father':rec_data.reciept_inv.stud_name.father_name,
        'skoollogo':skoollogo
    }

    pdf = render_to_pdf('fee/reciept_print.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def reprint_reciept(request,rec_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    try:
        rec = receipt_template.objects.get(school_name=sdata)
        rec_temp = rec.template
    except receipt_template.DoesNotExist:
        rec_temp= 'fee/reciept_show.html'

    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = fee_reciept.objects.get(pk=rec_id)
    amt_words = num2words(rec_data.paid_amt, lang ='en_IN').title()
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, rec_temp, context={'data': rec_data, 'sch_name': sdata,'skoollogo':skoollogo,'amt_words':amt_words})


@allowed_users(allowed_roles=['superadmin','Admin'])
def del_reciept(request,rec_id):
    rec_data = fee_reciept.objects.get(pk=rec_id)
    rec_data.reciept_inv.due_amt = rec_data.reciept_inv.due_amt + rec_data.paid_amt
    rec_data.reciept_inv.save(update_fields=["due_amt"])
    if rec_data.reciept_inv.fee_cat.fee_amount ==rec_data.reciept_inv.due_amt:
        rec_data.reciept_inv.status = 'Unpaid'
        rec_data.reciept_inv.save(update_fields=["status"])
    else:
        rec_data.reciept_inv.status = 'Partially Paid'
        rec_data.reciept_inv.save(update_fields=["status"])
    rec_data.delete()
    messages.success(request,'Reciept Deleted Successfully')
    return redirect('fee_reciepts')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def invoice_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    yr = academicyr.objects.get(acad_year=year, school_name=sdata)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'studname':
        data = addindfee.objects.filter(stud_name__first_name__istartswith=Searched,fee_cat__fees_school=sdata,fee_cat__ac_year=yr).order_by('stud_name')
    elif Searchby == 'admn_no':
        data = addindfee.objects.filter(stud_name__admn_no=Searched,fee_cat__fees_school=sdata)
    elif Searchby == 'cclass':
        tmpcls = sclass.objects.get(name=Searched,school_name=sdata)
        data = addindfee.objects.filter(class_name=tmpcls.id)
    elif Searchby == 'status':
        data = addindfee.objects.filter(status=Searched,fee_cat__fees_school=sdata)
    else:
        data = addindfee.objects.filter(student_status=Searched,fee_cat__fees_school=sdata)
    return render(request, 'fee/fee_details.html', context={'data':data,'skool': sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def invoices_download(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'studname':
        data = addindfee.objects.filter(stud_name__first_name__startswith=Searched)
    elif Searchby == 'admn_no':
        data = addindfee.objects.filter(stud_name__admn_no=Searched)
    elif Searchby == 'CClass':
        data = addindfee.objects.filter(class_name=Searched)
    else:
        data = addindfee.objects.filter(status=Searched)
    fdata={
        'data':data,
        'skool':sdata,
        'year':year
    }

    pdf = render_to_pdf('fee/fee_details_download.html', fdata)
    return HttpResponse(pdf, content_type='application/pdf')


def reciept_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'student_name':
        data = fee_reciept.objects.filter( reciept_inv__stud_name__first_name__icontains=Searched,reciept_inv__fee_cat__fees_school=sdata)
    elif Searchby == 'reciept_no':
        data = fee_reciept.objects(reciept_no=Searched,reciept_inv__fee_cat__fees_school=sdata)
    elif Searchby == 'reciept_date':
        data = fee_reciept.objects(reciept_date=Searched,reciept_inv__fee_cat__fees_school=sdata)
    else:
        data = fee_reciept.objects.filter(payment_id=Searched,reciept_inv__fee_cat__fees_school=sdata)
    return render(request, 'fee/fee_reciepts.html', context={'data': data, 'skool': sdata, 'year': year})


def temp_inv(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.filter(fee_cat__fees_school=sdata)
    cnt = 1
    for inv in data:
        inv.invoice_no = cnt
        cnt = cnt +1
        inv.save()
    return HttpResponse('Invoice updated')


def daily_collection(request):
    
    try:

        Searchby = request.POST['date_by']
        sch_id = request.session['sch_id']
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        tdy = datetime.date.today()
        tdy_fee = fee_reciept.objects.filter(reciept_date=Searchby,reciept_inv__fee_cat__fees_school=sdata)
        total_revenue_Cash = tdy_fee.filter(payment_type='Cash').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        total_revenue_Cheque = tdy_fee.filter(payment_type='Cheque').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        total_netbnk = tdy_fee.filter(payment_type='Net-Banking').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        total_BT = tdy_fee.filter(payment_type='Bank-Transfer').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        total_DD = tdy_fee.filter(payment_type='Demand-Draft').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        total_UPI = tdy_fee.filter(payment_type='UPI').aggregate(Sum('paid_amt'))['paid_amt__sum'] or 0
        
        tot_coll = sum(coll.paid_amt for coll in tdy_fee)

        context = {
            'tdy_fee': tdy_fee,
            'total_revenue_Cash':total_revenue_Cash,
            'total_revenue_Cheque':total_revenue_Cheque,
            'total_netbnk':total_netbnk,
            'total_BT':total_BT,
            'total_DD':total_DD,
            'total_UPI':total_UPI,
            'tot_coll': tot_coll,
            'skool':sdata
        }
    #     return render(request,'fee/collect_summary.html',context)
    # except:
    #     return HttpResponse("Error")

        pdf = render_to_pdf('fee/collect_summary.html', context)
        if pdf:
            return pdf
        else:
            return HttpResponse("Error generating PDF", status=500)


    except Exception as e:
        err_msg = f"{e}"
        return HttpResponse(err_msg)
 
def updateindfee_cat(request, feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.get(pk=feeind_id)
    feecat = fees.objects.filter(fees_school=sdata,ac_year=year)
    form = updateindfee_catform(request.POST or None, instance=data)
    form.fields['fee_cat'].queryset=feecat

    if form.is_valid():
        fee_cat_value = form.cleaned_data['fee_cat']
        instance = form.save(commit=False)
        instance.due_amt = fee_cat_value.fee_amount
        instance.save()

        messages.success(request, 'Record Updated Successfully')
        return redirect('invoices')

    return render(request, 'fee/updateindfee_cat.html', context={'form': form, 'skool': sdata})