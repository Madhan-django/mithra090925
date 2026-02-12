import datetime
import csv
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PettyCashExpense,CashSource,ExpenseCategory,PettyCashBalance
from .forms import NewCashSourceForm,NewPettyCashExpenseForm,NewExpenseCategoryForm
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from staff.models import staff
from django.contrib import messages
from datetime import date, timedelta
from .utils import render_to_pdf
from num2words import num2words
from django.contrib.auth.models import User
# Create your views here.

def pettycashExp(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = PettyCashExpense.objects.filter(petty_school=sdata,school_year=ayear).order_by('-date_spent')
    return render(request, 'pettycash/expense.html', context={'data': data, 'skool': sdata, 'year': year})

def cashsource(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = CashSource.objects.filter(source_school=sdata,school_year=ayear).order_by('-date_received')
    return render(request, 'pettycash/cashsource.html', context={'data': data, 'skool': sdata, 'year': year})

def addcashsource(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    petty_bal = PettyCashExpense.objects.filter(petty_school=sdata,school_year=ayear).order_by('-date_spent').first()
    usr = request.user


    initial_data = {
        'source_school': sdata,
        'received_by': usr,
        'school_year':ayear
    }

    if request.method == 'POST':
        form = NewCashSourceForm(request.POST)
        if form.is_valid():
            form_data = form.save()

            bal = PettyCashBalance.objects.filter(balance_school=sdata).order_by('-date').first()

            if bal:
                opening = bal.closing_balance
                closing = opening + form_data.amount
            else:
                opening = 0
                closing = form_data.amount

            PettyCashBalance.objects.create(
                date=form_data.date_received,
                opening_balance=opening,
                closing_balance=closing,
                balance_school=sdata,
                school_year=ayear
            )
            if petty_bal:
                petty_bal.balance = form_data.amount + petty_bal.balance
                petty_bal.save()
            messages.success(request, "Record Added Successfully")
            return redirect('cashsource')
        else:
            err = str(form.errors)
            return HttpResponse(err)

    else:
        form = NewCashSourceForm(initial=initial_data)

    return render(request, 'pettycash/newcash.html', {
        'form': form,
        'skool': sdata,
        'year': year
    })


def expensecategory(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = ExpenseCategory.objects.filter(expense_school=sdata).order_by('-id')
    return render(request, 'pettycash/exp_category.html', context={'data': data, 'skool': sdata, 'year': year})


def addexpense(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    record = PettyCashExpense.objects.filter(petty_school=sdata).order_by('-date_spent').first()
    open_bal = PettyCashBalance.objects.filter(balance_school=sdata).order_by('-date').first()
    usr = request.user
    date = datetime.date.today()
    if staff.objects.filter(staff_user=usr).exists():
        stf = staff.objects.get(staff_user=usr)
    else:
        stf=usr
    initial_data = {
        'petty_school':sdata,
        'balance':0,
        'approved_by':stf,
        'date_spent':date,
        'school_year':ayear


    }

    if request.method == 'POST':
        form = NewPettyCashExpenseForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if record:
                form_data.balance =record.balance-form_data.amount
                form_data.expense_no = record.expense_no+1
                form.save()
                messages.success(request,"Expense added Successfully")
                return redirect('pettycashExp')
            else:
                form_data.balance=open_bal.closing_balance-form_data.amount
                form_data.expense_no=1
                form.save()
                messages.success(request,"Expense added Successfully")
                return redirect('pettycashExp')

        else:
            err = str(form.errors)
            return HttpResponse(err)
    form1 = NewExpenseCategoryForm(initial={'expense_school': sdata})
    form = NewPettyCashExpenseForm(initial=initial_data)
    return render(request,'pettycash/add_expense.html',context={'form':form,'form1':form1,'skool':sdata,'year':year})

def addexpensecategory(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    if request.method == 'POST':
        form = NewExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category added Successfully")
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponse(status=404)

def balancesheet(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = PettyCashExpense.objects.filter(petty_school=sdata,school_year=ayear).order_by('-date_spent')
    balsum = []
    test = PettyCashExpense.objects.filter(
        petty_school=sdata,
        school_year=ayear
    ).order_by('-date_spent').values_list('date_spent', flat=True).distinct()
    for dt in test:
        first_record = PettyCashExpense.objects.filter(date_spent=dt,petty_school=sdata,school_year=ayear).first()
        last_record = PettyCashExpense.objects.filter(date_spent=dt,petty_school=sdata,school_year=ayear).last()
        if first_record and last_record:
            record = {
                'date': dt,
                'opening_balance': first_record.balance + first_record.amount,
                'closing_balance': last_record.balance,
            }
            balsum.append(record)

    return render(request, 'pettycash/balances.html', context={'data': balsum, 'skool': sdata, 'year': year})

def balancesheet_pdf(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)

    # Calculate cutoff date
    cutoff_date = date.today() - timedelta(days=30)

    # Get only last 31 days of records
    data = PettyCashExpense.objects.filter(
        petty_school=sdata,
        school_year=ayear,
        date_spent__gte=cutoff_date
    ).order_by('-date_spent')

    balsum = []
    test = data.values_list('date_spent', flat=True).distinct()

    for dt in test:
        first_record = PettyCashExpense.objects.filter(
            date_spent=dt,
            petty_school=sdata,
            school_year=ayear
        ).order_by('id').first()

        last_record = PettyCashExpense.objects.filter(
            date_spent=dt,
            petty_school=sdata,
            school_year=ayear
        ).order_by('-id').first()

        if first_record and last_record:
            record = {
                'date': dt,
                'opening_balance': first_record.balance + first_record.amount,
                'closing_balance': last_record.balance,
            }
            balsum.append(record)
    context = {
        'data': balsum,
        'skool': sdata,
        'year': year
    }

    pdf = render_to_pdf('pettycash/balance.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def pettycashExp_xl(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    cutoff_date = date.today() - timedelta(days=30)
    data = PettyCashExpense.objects.filter(petty_school=sdata,school_year=ayear,date_spent__gte=cutoff_date).order_by('-date_spent')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pettycash.csv"'
    writer = csv.writer(response)
    writer.writerow([sdata, ])
    writer.writerow(
        ['Date','Description','Category', 'Amount', 'Balance'])
    for obj in data:
        writer.writerow(
            [obj.date_spent, obj.description, obj.category, obj.amount, obj.balance])
    return response

def pettycashvoucher(request,exp_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    record = PettyCashExpense.objects.get(id=exp_id)
    amt_words = num2words(record.amount, lang='en_IN').title()
    return render(request,'pettycash/printvoucher.html',context={'skool':sdata,'year':year,'record':record,'amt_words':amt_words})
