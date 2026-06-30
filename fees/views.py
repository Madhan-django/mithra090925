import datetime
import io
import os
import time
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils import timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from num2words import num2words

from authenticate.decorators import allowed_users
from institutions.models import school
from setup.models import (
    academicyr,
    currentacademicyr,
    receipt_template,
    sclass,
    section,
)

from admission.models import students

from .forms import (
    addbulkfeeform,
    addfeerecieptform,
    addindfeeform,
    fee_addform,
    updateindfee_catform,
    updateindfeeform,
)

from .models import (
    PayUTransaction,
    SchoolPayUConfig,
    addindfee,
    del_fee_reciept,
    fee_reciept,
    fees,
)

from .payu_helper import generate_payu_hash, verify_payu_hash
from .utils import render_to_pdf

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




# @allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
# def addfeeind(request):
#
#     sch_id = request.session['sch_id']
#     sdata = school.objects.get(pk=sch_id)
#
#     yr = currentacademicyr.objects.get(school_name=sdata)
#     year = academicyr.objects.get(acad_year=yr,school_name=sdata)
#
#     data = fees.objects.filter(fees_school=sch_id,isactive='yes')
#     cdata = sclass.objects.filter(school_name=sch_id,acad_year=yr)
#     years = academicyr.objects.filter(school_name=sdata)
#
#     initial_data = {
#         'status':'Unpaid',
#         'invoice_no':0,
#         'due_amt':0,
#     }
#
#     if request.method == 'POST':
#         form = addindfeeform(request.POST)
#
#         if form.is_valid():
#
#             fee_ct = form.cleaned_data['fee_cat']
#             students = form.cleaned_data['stud_name']
#             concession = form.cleaned_data['concession']
#             class_name = form.cleaned_data['class_name']
#
#             for stud in students:
#
#                 addindfee.objects.create(
#                     fee_cat = fee_ct,
#                     class_name = class_name,
#                     stud_name = stud,
#                     concession = concession,
#                     status = 'Unpaid',
#                     due_amt = fee_ct.fee_amount,
#                     invoice_no = addindfee.objects.filter(fee_cat__fees_school=sch_id).count() + 1
#                 )
#
#             messages.success(request,"Fees Generated Successfully")
#             return redirect('invoices')
#
#         else:
#             messages.error(request,'Invalid form data')
#             return redirect('addindfee')
#
#     form = addindfeeform(initial=initial_data)
#     form1 = addbulkfeeform()
#
#     return render(request,'fee/addindfee.html',
#         context={'form':form,'data':data,'cdata':cdata,'skool':sdata,'form1':form1,'years':years})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addfeeind(request):

    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr,school_name=sdata)

    data = fees.objects.filter(fees_school=sch_id,isactive='yes')
    cdata = sclass.objects.filter(school_name=sch_id,acad_year=yr)
    years = academicyr.objects.filter(school_name=sdata)

    initial_data = {
        'status':'Unpaid',
        'invoice_no':0,
        'due_amt':0,
    }

    if request.method == 'POST':
        form = addindfeeform(request.POST)

        if form.is_valid():

            fee_ct = form.cleaned_data['fee_cat']
            concession = form.cleaned_data['concession']
            class_name = form.cleaned_data['class_name']

            students = request.POST.getlist('stud_name')  # ← change here

            for stud in students:

                addindfee.objects.create(
                    fee_cat = fee_ct,
                    class_name = class_name,
                    stud_name_id = stud,   # ← change here
                    concession = concession,
                    status = 'Unpaid',
                    due_amt = fee_ct.fee_amount,
                    invoice_no = addindfee.objects.filter(
                        fee_cat__fees_school=sch_id
                    ).count() + 1
                )

            messages.success(request,"Fees Generated Successfully")
            return redirect('invoices')

        else:
            messages.error(request,'Invalid form data')
            return redirect('addindfee')

    form = addindfeeform(initial=initial_data)
    form1 = addbulkfeeform()

    return render(request,'fee/addindfee.html',
        context={'form':form,'data':data,'cdata':cdata,'skool':sdata,'form1':form1,'years':years})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def fee_invoices(request):
    sch_id = request.session['sch_id']
    sdata= school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.filter(fee_cat__fees_school=sdata,fee_cat__isactive='yes').order_by('-id') [:100]
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


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def addbulkfee(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = fees.objects.filter(fees_school=sch_id, ac_year=year)
    if request.method == 'POST':
        form = addbulkfeeform(request.POST)
        if form.is_valid():
            fee_cat = form.cleaned_data['fee_cat']
            fee_class = form.cleaned_data['class_name']
            years = form.cleaned_data['years']
            stud = students.objects.filter(school_student=sch_id, class_name=fee_class, ac_year=year)
            print('stud', stud)
            inv_no = addindfee.objects.filter(fee_cat__fees_school=sch_id).count()
            for student in stud:
                inv_no = inv_no + 1

                addindfee.objects.create(fee_cat=fee_cat, class_name=fee_cat.iclass, stud_name=student, concession=0,
                                         status='Unpaid', invoice_no=inv_no, due_amt=fee_cat.fee_amount)
        messages.success(request, 'Fee has been Generated Successfully.')
        return redirect('invoices')
    form = addbulkfeeform()
    return render(request, 'fee/bulkfee.html', context={'form': form, 'skool': sdata, 'data': data})

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
        obj = form.save()
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
def addfeereciept(request, feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    recindfee = addindfee.objects.get(pk=feeind_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))

    if recindfee.status == 'Paid':
        messages.success(request, 'Fees Already paid')
        return redirect('invoices')

    # ✅ Only apply concession if it hasn't been applied yet
    if not recindfee.concession_apply and recindfee.concession > 0:
        # Apply discount on current due_amt (not gross)
        # This handles both fresh fees AND partially paid fees correctly
        net_payable = max(recindfee.due_amt - recindfee.concession, 0)
        recindfee.due_amt = net_payable
        recindfee.concession_apply = True
        recindfee.save(update_fields=["due_amt", "concession_apply"])
        recindfee.refresh_from_db()

    # If due becomes 0 after concession — mark paid
    if recindfee.due_amt == 0:
        recindfee.status = 'Paid'
        recindfee.save(update_fields=["status"])
        messages.success(request, 'Fee fully covered by concession.')
        return redirect('invoices')

    rec_no = fee_reciept.objects.all().count() + 1

    initial_data = {
        'reciept_inv': recindfee,
        'total': recindfee.due_amt,
        'paid_amt': recindfee.due_amt,
        'reciept_no': rec_no
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
                    recindfee.save(update_fields=["status", "due_amt", "concession_apply"])

                    new_record = form.save()
                    rec_data = fee_reciept.objects.get(id=new_record.id)

                    try:
                        rec = receipt_template.objects.get(school_name=sdata)
                        rec_temp = rec.template
                    except receipt_template.DoesNotExist:
                        rec_temp = 'fee/reciept_show.html'

                    amt_words = num2words(paid_amt1, lang='en_IN').title()

                    return render(request, rec_temp, context={
                        'data': rec_data,
                        'sch_name': sdata,
                        'skoollogo': skoollogo,
                        'amt_words': amt_words
                    })

                elif paid_amt1 < tot1:
                    recindfee.status = 'Partially Paid'
                    recindfee.due_amt = recindfee.due_amt - paid_amt1
                    recindfee.save(update_fields=["status", "due_amt", "concession_apply"])

                    new_record = form.save()
                    messages.success(request, 'Fee Paid Successfully')

                    rec_data = fee_reciept.objects.get(id=new_record.id)

                    try:
                        rec = receipt_template.objects.get(school_name=sdata)
                        rec_temp = rec.template
                    except receipt_template.DoesNotExist:
                        rec_temp = 'fee/reciept_show.html'

                    amt_words = num2words(paid_amt1, lang='en_IN').title()

                    return render(request, rec_temp, context={
                        'data': rec_data,
                        'sch_name': sdata,
                        'skoollogo': skoollogo,
                        'amt_words': amt_words
                    })

                else:
                    messages.warning(request, 'Invalid Amount')
                    return redirect('invoices')

        except Exception as e:
            error_message = str(e)
            return HttpResponse(f"Error: {error_message}", status=500)

    form = addfeerecieptform(initial=initial_data)
    form.fields['total'].widget.attrs['value'] = recindfee.due_amt
    form.fields['paid_amt'].widget.attrs['value'] = recindfee.due_amt
    form.fields['reciept_no'].widget.attrs['value'] = rec_no
    form.fields['reciept_inv'].widget.attrs['value'] = recindfee.pk

    return render(request, 'fee/addfeereciept.html', context={
        'form': form,
        'recindfee': recindfee,
        'skool': sdata
    })

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addfeereciept090426(request,feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    recindfee = addindfee.objects.get(pk=feeind_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))

    if recindfee.status=='Paid':
        messages.success(request,'Fees Already paid')
        return redirect('invoices')
    else:

        # Apply concession only once
        if not recindfee.concession_apply:
            if recindfee.due_amt >recindfee.concession:
                recindfee.due_amt = recindfee.due_amt - recindfee.concession
            else:
                recindfee.due_amt = 0

            recindfee.concession_apply = True
            recindfee.save(update_fields=["due_amt","concession_apply"])

            # reload updated object
            recindfee = addindfee.objects.get(pk=feeind_id)

        # If concession clears the balance
        if recindfee.due_amt == 0:
            recindfee.status = 'Paid'
            recindfee.save(update_fields=["status"])

        rec_no = fee_reciept.objects.all().count() + 1

        initial_data = {
            'reciept_inv': recindfee,
            'total': recindfee.due_amt,
            'paid_amt': recindfee.due_amt,
            'reciept_no': rec_no
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

                        return render(request,rec_temp, context={
                            'data': rec_data,
                            'sch_name': sdata,
                            'skoollogo':skoollogo,
                            'amt_words':amt_words
                        })

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

                        return render(request, rec_temp, context={
                            'data': rec_data,
                            'sch_name': sdata,
                            'skoollogo':skoollogo,
                            'amt_words':amt_words
                        })

                    else:
                        messages.warning(request, 'Invalid Amount')
                        return redirect('invoices')

            except Exception as e:
                error_message = str(e)
                return HttpResponse(f"Error: {error_message}", status=500)

    form = addfeerecieptform(initial=initial_data)

    return render(request,'fee/addfeereciept.html',context={
        'form':form,
        'recindfee':recindfee,
        'skool':sdata
    })
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


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','student'])
def reprint_reciept(request, rec_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    try:
        rec = receipt_template.objects.get(school_name=sdata)
        rec_temp = rec.template
    except receipt_template.DoesNotExist:
        rec_temp = 'fee/reciept_show.html'

    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = fee_reciept.objects.get(pk=rec_id)
    amt_words = num2words(rec_data.paid_amt, lang='en_IN').title()
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, rec_temp, context={
        'data':      rec_data,
        'sch_name':  sdata,
        'skoollogo': skoollogo,
        'amt_words': amt_words,
        'is_online': False,     # ← add this
    })


@allowed_users(allowed_roles=['superadmin','Admin'])
def del_reciept(request, rec_id):
    sch_id   = request.session['sch_id']
    sdata    = school.objects.get(pk=sch_id)
    rec_data = fee_reciept.objects.get(pk=rec_id)

    # ── Save to del_fee_reciept before deleting ──
    del_fee_reciept.objects.create(
        reciept_date    = rec_data.reciept_date,
        deletedate      = timezone.now().date(),
        reciept_no      = rec_data.reciept_no,
        reciept_student = rec_data.reciept_inv.stud_name,
        payment_type    = rec_data.payment_type,
        reciept_inv     = rec_data.reciept_inv,
        amount          = rec_data.paid_amt,
        usr             = request.user,
        sch             = sdata,
    )

    # ── Restore due amount ──
    rec_data.reciept_inv.due_amt = rec_data.reciept_inv.due_amt + rec_data.paid_amt
    rec_data.reciept_inv.save(update_fields=["due_amt"])

    # ── Update invoice status ──
    if rec_data.reciept_inv.fee_cat.fee_amount == rec_data.reciept_inv.due_amt:
        rec_data.reciept_inv.status = 'Unpaid'
        rec_data.reciept_inv.save(update_fields=["status"])
    else:
        rec_data.reciept_inv.status = 'Partially Paid'
        rec_data.reciept_inv.save(update_fields=["status"])

    rec_data.delete()
    messages.success(request, 'Receipt Deleted Successfully')
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
        data = addindfee.objects.filter(stud_name__first_name__istartswith=Searched,fee_cat__fees_school=sdata).order_by('stud_name','-fee_cat__ac_year')
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

def receipt_summary(request,feeind_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = fee_reciept.objects.filter(reciept_inv=feeind_id)
    stud = fee_reciept.objects.filter(reciept_inv=feeind_id).first()
    stud_name = stud.reciept_inv.stud_name
    return render(request,'fee/reciept_summary.html',context={'data': data, 'skool': sdata,'year':year,'stud_name':stud_name})


def con_correct(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = addindfee.objects.filter(fee_cat__fees_school=sdata)
    for dt in data:
        if dt.concession == 0:
            dt.concession_apply = False
            dt.save()
    messages.success(request, 'Record Updated Successfully')
    return redirect('invoices')



@login_required
def payu_initiate(request, invoice_id):
    usr     = request.user
    stud    = students.objects.get(usernm=usr)
    invoice = get_object_or_404(addindfee, id=invoice_id, stud_name=stud)

    # ── Get school PayU config ──
    try:
        payu_config = SchoolPayUConfig.objects.get(school=invoice.fee_cat.fees_school)
    except SchoolPayUConfig.DoesNotExist:
        return render(request, 'fee/payu_result.html', {
            'status':  'error',
            'message': 'Online payment is not configured for this school.',
        })

    if not payu_config.is_active:
        return render(request, 'fee/payu_result.html', {
            'status':  'error',
            'message': 'Online payment is not enabled for this school.',
        })

    txnid       = PayUTransaction.generate_txnid()
    amount      = str(invoice.due_amt)
    firstname   = stud.first_name
    phone       = str(stud.phone) if stud.phone else '9999999999'
    email       = stud.email if stud.email else f"{stud.admn_no}@mithran.in"
    productinfo = f"{invoice.fee_cat.invoice_title} - {stud.first_name} {stud.last_name}"

    success_url = request.build_absolute_uri('/fees/payu/success/')
    failure_url = request.build_absolute_uri('/fees/payu/failure/')

    params = {
        'key':         payu_config.merchant_key,   # ← per school
        'txnid':       txnid,
        'amount':      amount,
        'productinfo': productinfo,
        'firstname':   firstname,
        'email':       email,
        'phone':       phone,
        'surl':        success_url,
        'furl':        failure_url,
        'udf1':        str(invoice.id),
        'udf2':        str(stud.id),
        'udf3':        str(payu_config.school.id),  # store school id for callback
        'udf4':        '',
        'udf5':        '',
    }

    params['hash'] = generate_payu_hash(params, payu_config.merchant_salt)  # ← per school

    PayUTransaction.objects.create(
        txnid=txnid,
        invoice=invoice,
        student=stud,
        amount=invoice.due_amt,
        status='initiated'
    )

    return render(request, 'fee/payu_redirect.html', {
        'params':   params,
        'payu_url': payu_config.base_url,           # ← per school
    })



@csrf_exempt
def payu_success(request):
    if request.method != 'POST':
        return redirect('student_fee_invoice')

    response_data  = request.POST.dict()
    received_hash  = response_data.pop('hash', '')

    # ── Get school config using udf3 ──
    school_id = response_data.get('udf3')
    try:
        payu_config = SchoolPayUConfig.objects.get(school__id=school_id)
    except SchoolPayUConfig.DoesNotExist:
        return render(request, 'fee/payu_result.html', {
            'status':  'error',
            'message': 'School payment config not found.',
        })

    # ── Verify hash (skip in test mode) ──
    if not payu_config.is_test:
        generated_hash = verify_payu_hash(response_data, payu_config.merchant_salt)
        if received_hash.lower() != generated_hash.lower():
            return render(request, 'fee/payu_result.html', {
                'status':  'error',
                'message': 'Payment verification failed. Please contact school admin.',
            })

    txnid      = response_data.get('txnid')
    payu_txnid = response_data.get('mihpayid')
    invoice_id = response_data.get('udf1')
    status     = response_data.get('status')

    try:
        txn     = PayUTransaction.objects.get(txnid=txnid)
        invoice = addindfee.objects.get(id=invoice_id)
    except (PayUTransaction.DoesNotExist, addindfee.DoesNotExist):
        return render(request, 'fee/payu_result.html', {
            'status':  'error',
            'message': 'Transaction record not found.',
        })

    if status == 'success':
        txn.status     = 'success'
        txn.payu_txnid = payu_txnid
        txn.save()

        invoice.status  = 'Paid'
        invoice.due_amt = 0
        invoice.save()

        receipt = _auto_generate_receipt(invoice, txn)

        if receipt is None:
            return render(request, 'fee/payu_result.html', {
                'status':  'error',
                'message': 'Payment successful but receipt generation failed. Contact admin.',
            })

        return redirect(reverse('online_reciept', kwargs={'rec_id': receipt.id}))

    elif status == 'pending':
        txn.status = 'pending'
        txn.save()
        return render(request, 'fee/payu_result.html', {
            'status':  'pending',
            'message': 'Payment is pending. Please wait for confirmation.',
            'txnid':   txnid,
        })

    else:
        txn.status = 'failure'
        txn.save()
        return render(request, 'fee/payu_result.html', {
            'status':  'failure',
            'message': 'Payment failed. Please try again.',
            'txnid':   txnid,
        })

@csrf_exempt
def payu_successbak(request):
    if request.method != 'POST':
        return redirect('student_fee_invoice')

    response_data  = request.POST.dict()
    received_hash  = response_data.pop('hash', '')

    # ── Only verify in production, skip for test ──
    if not settings.PAYU_TEST_MODE:
        generated_hash = verify_payu_hash(response_data, settings.PAYU_MERCHANT_SALT)
        if received_hash.lower() != generated_hash.lower():
            return render(request, 'fee/payu_result.html', {
                'status':  'error',
                'message': 'Payment verification failed. Please contact school admin.',
            })

    txnid      = response_data.get('txnid')
    payu_txnid = response_data.get('mihpayid')
    invoice_id = response_data.get('udf1')
    status     = response_data.get('status')

    try:
        txn     = PayUTransaction.objects.get(txnid=txnid)
        invoice = addindfee.objects.get(id=invoice_id)

        if status == 'success':
            txn.status     = 'success'
            txn.payu_txnid = payu_txnid
            txn.save()

            invoice.status  = 'Paid'
            invoice.due_amt = 0
            invoice.save()

            receipt = _auto_generate_receipt(invoice, txn)
            return redirect(reverse('online_reciept', kwargs={'rec_id': receipt.id}))

        else:
            txn.status = 'pending'
            txn.save()
            return render(request, 'fee/payu_result.html', {
                'status':  'pending',
                'message': 'Payment is pending. Please wait for confirmation.',
                'txnid':   txnid,
            })

    except (PayUTransaction.DoesNotExist, addindfee.DoesNotExist):
        return render(request, 'fee/payu_result.html', {
            'status':  'error',
            'message': 'Transaction record not found.',
        })



@csrf_exempt
def payu_failure(request):
    if request.method != 'POST':
        return redirect('student_fee_list')

    response_data = request.POST.dict()
    txnid         = response_data.get('txnid')

    try:
        txn        = PayUTransaction.objects.get(txnid=txnid)
        txn.status = 'failure'
        txn.save()
    except PayUTransaction.DoesNotExist:
        pass

    return render(request, 'fee/payu_result.html', {
        'status':  'failure',
        'message': 'Payment failed. Please try again or contact school admin.',
        'txnid':   txnid,
        'reason':  response_data.get('error_Message', 'Unknown error'),
    })


def _auto_generate_receipt(invoice, txn):
    from .models import fee_reciept
    from datetime import date

    try:
        last    = fee_reciept.objects.order_by('-reciept_no').first()
        next_no = (last.reciept_no + 1) if last else 1

        receipt, created = fee_reciept.objects.get_or_create(
            reciept_inv=invoice,
            defaults={
                'reciept_date': date.today(),
                'reciept_no':   next_no,
                'payment_type': 'Online',
                'payment_id':   txn.payu_txnid,
                'total':        int(invoice.fee_cat.fee_amount),
                'paid_amt':     int(invoice.fee_cat.fee_amount),
                'note':         f'PayU txnid: {txn.txnid}',
            }
        )
        print("RECEIPT CREATED:", receipt, receipt.id)
        return receipt
    except Exception as e:
        print("RECEIPT ERROR:", e)
        return None

@login_required
def payu_result_success(request, receipt_id):
    from .models import fee_reciept
    receipt = get_object_or_404(fee_reciept, id=receipt_id)
    return render(request, 'fee/payu_result.html', {
        'status':  'success',
        'message': 'Payment successful! Your receipt has been generated.',
        'receipt': receipt,
        'invoice': receipt.reciept_inv,
        'amount':  receipt.paid_amt,
        'txnid':   receipt.payment_id,
    })

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def payu_config_view(request):
    sch_id = request.session['sch_id']
    sdata  = school.objects.get(pk=sch_id)

    config, _ = SchoolPayUConfig.objects.get_or_create(
        school=sdata,
        defaults={'merchant_key': '', 'merchant_salt': '', 'is_active': False}
    )

    if request.method == 'POST':
        config.merchant_key  = request.POST.get('merchant_key', '').strip()
        config.merchant_salt = request.POST.get('merchant_salt', '').strip()
        config.is_active     = request.POST.get('is_active') == 'on'
        config.is_test       = request.POST.get('is_test') == 'on'
        config.save()
        messages.success(request, 'PayU configuration saved successfully.')
        return redirect('payu_config_view')

    return render(request, 'fee/payu_config.html', {
        'config': config,
        'skool':  sdata,
    })

@login_required
def onlinereprint_reciept(request, rec_id):
    usr     = request.user
    stud    = students.objects.get(usernm=usr)
    rec_data = fee_reciept.objects.get(pk=rec_id)

    # Security check — ensure receipt belongs to this student
    if rec_data.reciept_inv.stud_name != stud:
        return redirect('student_fee_invoice')

    sdata     = rec_data.reciept_inv.fee_cat.fees_school
    amt_words = num2words(rec_data.paid_amt, lang='en_IN').title()
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))

    try:
        rec = receipt_template.objects.get(school_name=sdata)
        rec_temp = rec.template
    except receipt_template.DoesNotExist:
        rec_temp = 'fee/reciept_show.html'

    return render(request, rec_temp, context={
        'data':      rec_data,
        'sch_name':  sdata,
        'skoollogo': skoollogo,
        'amt_words': amt_words,
        'is_online': True,      # ← student portal flag
    })