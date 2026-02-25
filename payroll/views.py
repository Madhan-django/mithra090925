from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.urls import reverse
from django.db import transaction
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from staff.models import staff
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Department,Designation,PayrollEmployee,PayrollBank,Allowance,Deduction,Employee_allowance_Details,Employee_deduction_Details,Loan,Attendance,Holiday,PayrollSettings,PayrollMonthly
from .forms import add_deptform,add_desgform,PayrollEmployeeForm,Allowanceform,Deductionform,NewLoanForm,add_holidayform,PayrollSettingsForm
import math
from dateutil.relativedelta import relativedelta
from django.db import connection
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.utils.timezone import now
from django.utils import timezone
from datetime import date
from openpyxl import Workbook
from django.db.models import Sum
from decimal import Decimal
import calendar

# Create your views here.
def PDept_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Department.objects.filter(sch=sdata)
    return render(request, 'payroll/DeptList.html', context={'data': data, 'skool': sdata, 'year': year})

def PDept_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'sch':sdata
    }
    if request.method == 'POST':
        form  = add_deptform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added successfully")
            return redirect('department')
    else:
        form = add_deptform(initial=initial_data)
    return render(request,'payroll/add_dept.html',context={'form':form,'skool':sdata,'year':year})

def PDept_update(request,dept_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Department.objects.get(id=dept_id)
    if request.method == 'POST':
        form = add_deptform(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully")
            return redirect('department')
    else:
        form  = add_deptform(instance = data)
    return render(request,'payroll/add_dept.html',context={'form':form,'skool':sdata,'year':year})

def PDept_del(request,dept_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Department.objects.get(id=dept_id)
    data.delete()
    messages.success(request,"Department deleted successfully")
    return redirect('department')

def PDesignation_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Designation.objects.filter(department__sch=sdata)
    return render(request, 'payroll/DesignationList.html', context={'data': data, 'skool': sdata, 'year': year})

def PDesignation_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    dept = Department.objects.filter(sch=sdata)
    if request.method == 'POST':
        form = add_desgform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Designation added successfully")
            return redirect('designation')

    form = add_desgform()
    return render(request,'payroll/add_desg.html',context={'form':form,'dept':dept,'skool':sdata,'year':year})

def PDesignation_update(request, desg_id):
    sch_id = request.session.get('sch_id')  # Use .get() to avoid KeyError
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    dept = Department.objects.filter(sch=sdata)
    desg = Designation.objects.get(id=desg_id)
    if request.method == 'POST':
        form = add_desgform(request.POST or None, instance=desg)  # Corrected form handling
        if form.is_valid():
            form.save()
            messages.success(request, "Designation Updated successfully")  # Fixed messages.success
            return redirect('designation')
    form = add_desgform(instance=desg)
    return render(request, 'payroll/add_desg.html',context={'form':form,'skool': sdata,'dept':dept, 'year': year})

def PDesignation_del(request, desg_id):
    sch_id = request.session.get('sch_id')  # Use .get() to avoid KeyError
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    desg = Designation.objects.get(id=desg_id)
    desg.delete()
    messages.success(request,"Designation Deleted Successfully")



def PEmployees(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = PayrollEmployee.objects.filter(emp_sch=sdata,status= True)
    return render(request, 'payroll/PEmployees.html', context={'data': data, 'skool': sdata, 'year': year})


def PEmployee_add(request):
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        dept = Department.objects.filter(sch=sdata)
        desg = Designation.objects.filter(department__sch=sdata)

    except (school.DoesNotExist, currentacademicyr.DoesNotExist, academicyr.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    # Always define the forms to avoid "referenced before assignment" errors
    intial_data = {
         'emp_sch': sdata
    }
    emp_form = PayrollEmployeeForm(initial=intial_data)
    formset = PayrollBankFormSet()

    if request.method == 'POST':
        emp_form = PayrollEmployeeForm(request.POST)

        if emp_form.is_valid():
            employee = emp_form.save(commit=False)  # Save but don't commit
            employee.school = sdata  # Assign related school instance
            employee.save()  # Now save with school

            formset = PayrollBankFormSet(request.POST, instance=employee)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Employee added successfully")
                return redirect('Employees')
            else:
                messages.error(request, "Bank details contain errors")
        else:
            messages.error(request, "Employee details contain errors")
            print(emp_form.errors)  # Debugging error messages

    return render(request, 'payroll/add_Employee.html', {
        'emp_form': emp_form,
        'formset': formset,
        'dept': dept,
        'desg': desg,
        'skool': sdata,
        'year': year
    })


def PEmployee_update(request, emp_id):
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        employee = PayrollEmployee.objects.get(pk=emp_id, emp_sch=sdata)  # Ensure employee belongs to the school
        dept = Department.objects.filter(sch=sdata)
        desg = Designation.objects.filter(department__sch=sdata)
    except (school.DoesNotExist, PayrollEmployee.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    if request.method == 'POST':
        emp_form = PayrollEmployeeForm(request.POST, instance=employee)
        formset = payrollBankFormupdate(request.POST, instance=employee)

        if emp_form.is_valid() and formset.is_valid():
            emp_form.save()
            formset.save()
            messages.success(request, "Employee details updated successfully")
            return redirect('Employees')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        emp_form = PayrollEmployeeForm(instance=employee)
        formset = payrollBankFormupdate(instance=employee)

    return render(request, 'payroll/update_Employee.html', {
        'emp_form': emp_form,
        'formset': formset,
        'dept': dept,
        'desg': desg,
        'skool': sdata,
        'employee': employee
    })
def PEmployee_del(request,emp_id):
    emp = PayrollEmployee.objects.get(id=emp_id)
    emp.delete()
    messages.success(request, "Employee Deleted successfully")
    return redirect('Employees')


def Allowance_list(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Allowance.objects.filter(sch=sdata)
    return render(request,'payroll/AllowanceList.html',context={'data':data,'skool':sdata,'year':year})



def add_Allowance(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
            'sch':sdata
        }
    if request.method =='POST':
        form = Allowanceform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Allowance created Successfully')
            return redirect('allowance')
    form = Allowanceform(initial=initial_data)
    return render(request,'payroll/add_allowance.html',context={'form':form,'skool':sdata})


def update_Allowance(request, allowance_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (school.DoesNotExist, currentacademicyr.DoesNotExist, academicyr.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    allowance = get_object_or_404(Allowance, id=allowance_id, sch=sdata)

    if request.method == 'POST':
        form = Allowanceform(request.POST, instance=allowance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allowance updated successfully!')
            return redirect('allowance')  # Redirect to allowance list after update
        else:
            messages.error(request, 'Error updating allowance.')

    else:
        form = Allowanceform(instance=allowance)

    return render(request, 'payroll/update_allowance.html', {
        'form': form,
        'skool': sdata,
        'allowance': allowance
    })


def del_Allowance(request, allowance_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (school.DoesNotExist, currentacademicyr.DoesNotExist, academicyr.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    allowance = get_object_or_404(Allowance, id=allowance_id, sch=sdata)
    allowance.delete()
    messages.success(request,'Allowance Deleted Successfully')
    return redirect('allowance')

def Deduction_list(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Deduction.objects.filter(sch=sdata)
    return render(request,'payroll/DeductionList.html',context={'data':data,'skool':sdata,'year':year})



def add_Deduction(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
            'sch':sdata
        }
    if request.method =='POST':
        form = Deductionform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Deduction created Successfully')
            return redirect('deduction')
        else:
            return HttpResponse(form.errors)
    form = Deductionform(initial=initial_data)
    return render(request,'payroll/add_deduction.html',context={'form':form,'skool':sdata})


def update_Deduction(request, deduction_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (school.DoesNotExist, currentacademicyr.DoesNotExist, academicyr.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    deduction = get_object_or_404(Deduction, id=deduction_id, sch=sdata)

    if request.method == 'POST':
        form = Deductionform(request.POST, instance=deduction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deduction updated successfully!')
            return redirect('deduction')  # Redirect to allowance list after update
        else:
            return HttpResponse(form.errors)

    else:
        form = Deductionform(instance=deduction)

    return render(request, 'payroll/update_deduction.html', {
        'form': form,
        'skool': sdata,
        'deduction': deduction
    })


def del_Deduction(request, deduction_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        return HttpResponse("School ID not found in session", status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except (school.DoesNotExist, currentacademicyr.DoesNotExist, academicyr.DoesNotExist) as e:
        return HttpResponse(f"Data not found: {e}", status=400)

    deduction = get_object_or_404(Deduction, id=deduction_id, sch=sdata)
    deduction.delete()
    messages.success(request,'Deduction Deleted Successfully')
    return redirect('deduction')


def apply_Allowance(request, allowance_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        messages.error(request, "School ID not found in session.")
        return redirect('allowance')

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        emps = PayrollEmployee.objects.filter(emp_sch=sdata)
        allow = Allowance.objects.get(id=allowance_id)

        if not emps.exists():
            messages.error(request, "No Employees Available")
            return redirect('allowance')

        for emp in emps:
            # Check if the allowance already exists for the employee
            exists = Employee_allowance_Details.objects.filter(employee_name=emp, allowance_name=allow).exists()

            if not exists:
                basic_salary = emp.basic_salary if emp.basic_salary else 0
                allow_percentage = allow.allow_percentage if allow.allow_percentage else 0
                amt = (basic_salary * allow_percentage / 100) if allow_percentage > 0 else 0
                Employee_allowance_Details.objects.create(employee_name=emp, allowance_name=allow, amount=amt)

        messages.success(request, "Allowance Applied to Employees")

    except school.DoesNotExist:
        messages.error(request, "School not found.")
    except Allowance.DoesNotExist:
        messages.error(request, "Allowance not found.")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect('allowance')


def apply_Deduction(request, deduction_id):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        messages.error(request, "School ID not found in session.")
        return redirect('deduction')

    try:
        sdata = school.objects.get(pk=sch_id)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        emps = PayrollEmployee.objects.filter(emp_sch=sdata)
        deduct = Deduction.objects.get(id=deduction_id)

        if not emps.exists():
            messages.error(request, "No Employees Available")
            return redirect('deduction')

        for emp in emps:
            # Check if deduction already exists for the employee
            exists = Employee_deduction_Details.objects.filter(
                employee_name=emp,
                deduction_name=deduct
            ).exists()

            if exists:
                continue

            # Choose salary based on ciel_based_on
            salary_to_check = emp.gross_salary if deduct.ciel_based_on == 'gross' else (
                emp.basic_salary if deduct.ciel_based_on == 'basic' else emp.gross_salary
            )

            # Ceiling check
            if (deduct.ciel_min is not None and salary_to_check < deduct.ciel_min) or \
               (deduct.ciel_max is not None and salary_to_check > deduct.ciel_max):
                continue  # Skip if not eligible

            # Calculate amount
            if deduct.method == 'percentage_basic':
                amount = (emp.basic_salary * deduct.value) / 100
            elif deduct.method == 'percentage_gross':
                amount = (emp.gross_salary * deduct.value) / 100
            elif deduct.method == 'fixed_amount':
                amount = deduct.value
            elif deduct.method == 'emi':
                amount = deduct.emi_amount or 0
            else:
                amount = 0

            # Create entry
            Employee_deduction_Details.objects.create(
                employee_name=emp,
                deduction_name=deduct,
                amount=amount,
                emi_amount=deduct.emi_amount or 0,
                balance=deduct.balance or 0,
                start_date=deduct.start_date,
                end_date=deduct.end_date,
                active=True
            )

        messages.success(request, "Deduction applied to all eligible employees.")
        return redirect('deduction')

    except school.DoesNotExist:
        messages.error(request, "School not found.")
    except Deduction.DoesNotExist:
        messages.error(request, "Deduction not found.")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect('deduction')


def Employee_Salary_Record(request,Employee_id):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    emp = PayrollEmployee.objects.get(id=Employee_id)
    emp_allow_exist = Employee_allowance_Details.objects.filter(employee_name=emp).exists()
    if not emp_allow_exist:
        addition = Allowance.objects.filter(sch=sdata)

        for add in addition:
            Employee_allowance_Details.objects.create(
                employee_name=emp,
                allowance_name=add,
                amount=0
               )
    emp_deduct_exist = Employee_allowance_Details.objects.filter(employee_name=emp).exists()
    if not emp_allow_exist:
        subtraction = Deduction.objects.filter(sch=sdata)
        for sub in subtraction:
            Employee_deduction_Details.objects.create(
                employee_name=emp,
                deduction_name=sub,
                amount=0,
                emi_amount=0,
                balance=0,
                start_date="2900-01-01",
                end_date="2900-01-01",
                active=True
            )

    emp_allowance = Employee_allowance_Details.objects.filter(employee_name=emp)
    emp_deduction = Employee_deduction_Details.objects.filter(employee_name=emp)
    emp_loan = Loan.objects.filter(employee=emp).exclude(remaining_amount = 0)
    bank_detail = PayrollBank.objects.get(CustName=emp)
    return render(request,'payroll/Employee_Salary_Records.html',context={'skool':sdata,'year':year,'emp':emp,'allowances':emp_allowance,'deductions':emp_deduction,'emp_loan':emp_loan,'bank_detail':bank_detail})

@csrf_exempt
def update_salary(request):
    if request.method == 'POST':
        record_id = request.POST.get('id')
        record_type = request.POST.get('type')
        new_value = request.POST.get('value')

        try:
            new_value = float(new_value)  # Ensure valid numeric input
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid value'})

        if record_type == 'allowance':
            record = get_object_or_404(Employee_allowance_Details, id=record_id)
        elif record_type == 'deduction':
            record = get_object_or_404(Employee_deduction_Details, id=record_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid record type'})

        record.amount = new_value
        record.save()
        return JsonResponse({'status': 'success', 'message': 'Updated successfully'})

    return JsonResponse({'status': 'error','message': 'Invalid request'})


def Loan_List(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    loans = Loan.objects.filter(employee__emp_sch=sdata).exclude(remaining_amount=0)
    return render(request,'payroll/LoanList.html',context={'skool':sdata,'year':year,'loans':loans})

def New_Loan(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    emps = PayrollEmployee.objects.filter(emp_sch=sdata)
    if request.method == 'POST':
        form = NewLoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)  # Get form data but don't save yet
            start_date = form.cleaned_data['start_date']
            loan_amount = form.cleaned_data['loan_amount']
            emi = form.cleaned_data['monthly_installment']
            tenure = math.ceil(loan_amount/emi)
            loan.end_date = start_date + relativedelta(months=tenure)

            form.save()
            messages.success(request,"New Loan updated Successfully")
            return redirect('loan_list')
        else:
            return HttpResponse(form.errors)
    form = NewLoanForm()
    return render(request,'payroll/add_loan.html',context={'skool':sdata,'year':year,'form':form,'emps':emps})


def Del_Loan(request,loan_id):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Loan.objects.get(id=loan_id)
    data.delete()
    messages.success(request,'Loan Deleted Successfully')
    return redirect('loan_list')

def daily_attendance_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    selected_date = request.GET.get('date')
    export = request.GET.get('export')

    attendance_list = []

    if selected_date:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()

        records = Attendance.objects.filter(
            date=date_obj
        ).select_related('staff', 'staff__department')

        for record in records:

            # Convert to Local Time for Display
            local_in = timezone.localtime(record.first_in) if record.first_in else None
            local_out = timezone.localtime(record.last_out) if record.last_out else None

            # Format Work Duration
            if record.work_duration:
                total_seconds = int(record.work_duration.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                work_hours = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                work_hours = ""

            attendance_list.append({
                "user_id": record.staff.BioCode,
                "staff": f"{record.staff.first_name} {record.staff.last_name}",
                "Designation": record.staff.desg or "",
                "Department": record.staff.department.name if record.staff.department else "",
                "in_time": local_in,
                "out_time": local_out,
                "work_hours": work_hours,
                "late": record.late,           # ✅ From DB (No recalculation)
                "mispunch": record.mis_punch,
                "status": record.status,
                "punch_count": record.punch_count
            })

    # ================== EXPORT TO EXCEL ==================
    if export == "excel" and selected_date:

        wb = Workbook()
        ws = wb.active
        ws.title = "Daily Attendance"
        ws.append([sdata.name])
        ws.append([])
        headers = [
            "User ID",
            "Name",
            "Desg",
            "Dept",
            "In Time",
            "Out Time",
            "Work Hours",
            "Late",
            "Mis Punch",
            "Status",
            "Punch Count"
        ]
        ws.append(headers)

        for data in attendance_list:
            ws.append([
                data["user_id"],
                data["staff"],
                data["Designation"],
                data["Department"],
                data["in_time"].strftime("%d-%m-%Y %H:%M:%S") if data["in_time"] else "",
                data["out_time"].strftime("%d-%m-%Y %H:%M:%S") if data["out_time"] else "",
                data["work_hours"],
                "YES" if data["late"] else "NO",
                "YES" if data["mispunch"] else "NO",
                data["status"],
                data["punch_count"]
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="daily_attendance_{selected_date}.xlsx"'
        )

        wb.save(response)
        return response

    return render(request, "payroll/dayattendance.html", {
        "attendance": attendance_list,
        "selected_date": selected_date,
        "skool":sdata,
        "year":year
    })


def import_employees(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            messages.error(request, "Please upload an Excel file.")
            return redirect("import_employees")

        wb = openpyxl.load_workbook(file)
        ws = wb.active

        errors = []
        employees_to_create = []
        excel_emp_codes = set()

        for index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):

            (
                emp_code,
                name,
                department_name,
                designation_name,
                date_of_joining,
                emp_type,
                basic_salary,
                gross_salary,
                contact,
                email
            ) = row

            row_errors = []

            # ----------------------
            # Required Field Check
            # ----------------------
            if not emp_code:
                row_errors.append("Emp Code is required")

            if not name:
                row_errors.append("Name is required")

            if not department_name:
                row_errors.append("Department is required")

            if not designation_name:
                row_errors.append("Designation is required")

            # ----------------------
            # Duplicate Check (Excel)
            # ----------------------
            if emp_code in excel_emp_codes:
                row_errors.append("Duplicate Emp Code in Excel")
            else:
                excel_emp_codes.add(emp_code)

            # ----------------------
            # Duplicate Check (Database)
            # ----------------------
            if PayrollEmployee.objects.filter(emp_code=emp_code).exists():
                row_errors.append("Emp Code already exists in system")

            # ----------------------
            # ForeignKey Validation
            # ----------------------
            try:
                department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                row_errors.append(f"Department '{department_name}' not found")
                department = None

            try:
                designation = Designation.objects.get(name=designation_name)
            except Designation.DoesNotExist:
                row_errors.append(f"Designation '{designation_name}' not found")
                designation = None

            # ----------------------
            # Date Validation
            # ----------------------
            if isinstance(date_of_joining, datetime):
                date_of_joining = date_of_joining.date()
            else:
                row_errors.append("Invalid Date format")

            # ----------------------
            # Salary Validation
            # ----------------------
            try:
                basic_salary = float(basic_salary)
                gross_salary = float(gross_salary)
            except:
                row_errors.append("Invalid salary format")

            # ----------------------
            # Collect Errors
            # ----------------------
            if row_errors:
                errors.append(f"Row {index}: " + ", ".join(row_errors))
            else:
                employees_to_create.append(
                    PayrollEmployee(
                        emp_code=emp_code,
                        name=name,
                        department=department,
                        designation=designation,
                        date_of_joining=date_of_joining,
                        emp_type=emp_type,
                        basic_salary=basic_salary,
                        gross_salary=gross_salary,
                        contact=contact,
                        email=email,
                        emp_sch_id=request.session.get("sch_id")
                    )
                )

        # ============================
        # If Any Errors → Show Errors
        # ============================
        if errors:
            for error in errors:
                messages.error(request, error)

            messages.error(request, "Import failed. Please fix errors and try again.")
            return redirect("import_employees")

        # ============================
        # If No Errors → Save All
        # ============================
        with transaction.atomic():
            PayrollEmployee.objects.bulk_create(employees_to_create)

        messages.success(request, "All Employees Imported Successfully.")
        return redirect("import_employees")

    return render(request, "payroll/import_employees.html")


def export_employee_sample(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Employee Sample"

    # Header Row
    headers = [
        "emp_code",
        "name",
        "department",
        "designation",
        "date_of_joining (YYYY-MM-DD)",
        "emp_type",
        "basic_salary",
        "gross_salary",
        "contact",
        "email"
    ]

    ws.append(headers)

    # Sample Row
    ws.append([
        "EMP001",
        "John Doe",
        "Computer Science",
        "Lecturer",
        "2024-06-01",
        "Teaching",
        25000,
        35000,
        "9876543210",
        "john@example.com"
    ])

    # Optional: Make header bold
    for cell in ws[1]:
        cell.font = cell.font.copy(bold=True)

    # Auto column width
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column_letter].width = max_length + 3

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="employee_import_sample.xlsx"'

    wb.save(response)
    return response


# Rules
MIN_WORK_HOURS = timedelta(hours=8)
GRACE_MINUTES = 0   # Change to 10 if you want grace time


def sync_attendance_from_device(request):

    today = now().date()

    last_record = Attendance.objects.order_by('-date').first()

    if last_record:
        start_date = last_record.date + timedelta(days=1)
    else:
        start_date = datetime(2024, 1, 1).date()

    if start_date > today:
        print("Already up to date")
        return redirect('day_attendance')

    current_date = start_date

    while current_date <= today:

        table_name = f"devicelogs_{current_date.month}_{current_date.year}"

        query = f"""
            SELECT
                UserId,
                MIN(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS in_time,
                MAX(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS out_time,
                COUNT(*) as punch_count
            FROM {table_name}
            WHERE DATE(CONVERT_TZ(LogDate, '+00:00', '+05:30')) = %s
            GROUP BY UserId
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [current_date])
                rows = cursor.fetchall()
        except Exception:
            current_date += timedelta(days=1)
            continue

        for row in rows:
            user_id, in_time, out_time, punch_count = row

            try:
                stf = staff.objects.select_related('shift').get(BioCode=user_id)
            except staff.DoesNotExist:
                continue

            status = "PRESENT"
            mispunch = False
            late = False
            work_duration = None

            # ================= MIS PUNCH =================
            if punch_count == 1:
                status = "MIS_PUNCH"
                mispunch = True

            # ================= NORMAL CASE =================
            elif in_time and out_time:

                work_duration = out_time - in_time

                # HALF DAY
                if work_duration < MIN_WORK_HOURS:
                    status = "HALF_DAY"

                # ================= SHIFT BASED LATE =================
                if stf.shift:
                    shift_time = stf.shift.start_time
                else:
                    shift_time = datetime.strptime("09:00:00", "%H:%M:%S").time()

                shift_datetime = datetime.combine(current_date, shift_time)
                grace_datetime = shift_datetime + timedelta(minutes=GRACE_MINUTES)

                if in_time > grace_datetime:
                    late = True

            Attendance.objects.update_or_create(
                staff=stf,
                date=current_date,
                defaults={
                    "sch": stf.staff_school,
                    "first_in": in_time,
                    "last_out": out_time,
                    "punch_count": punch_count,
                    "work_duration": work_duration,
                    "late": late,
                    "mis_punch": mispunch,
                    "status": status,
                }
            )

        current_date += timedelta(days=1)

    messages.success(request, "Sync Completed Successfully")
    return redirect('day_attendance')


# def Staff_Monthly_Attendance(request):
#
#     sch_id = request.session.get('sch_id')
#     sdata = get_object_or_404(school, pk=sch_id)
#
#     yr = currentacademicyr.objects.get(school_name=sdata)
#     acad_year = academicyr.objects.get(acad_year=yr, school_name=sdata)
#     try:
#         payroll_settings = sdata.payroll_settings
#     except PayrollSettings.DoesNotExist:
#         payroll_settings = None
#     employees = staff.objects.filter(staff_school=sch_id)
#
#     employee_id = request.GET.get("employee")
#     month = int(request.GET.get("month", date.today().month))
#     year = int(request.GET.get("year", date.today().year))
#
#     selected_employee = None
#     attendance_list = []
#     status_choices = Attendance.STATUS_CHOICES
#
#     total_present = 0
#     total_absent = 0
#     total_half = 0
#     total_late = 0
#     total_mis = 0
#
#     if employee_id:
#
#         selected_employee = get_object_or_404(staff, id=employee_id)
#         total_days = calendar.monthrange(year, month)[1]
#
#         # =====================================================
#         # ✅ POST SECTION
#         # =====================================================
#         if request.method == "POST":
#
#             for day in range(1, total_days + 1):
#
#                 attendance_date = date(year, month, day)
#
#                 selected_status = request.POST.get(f"status_{day}")
#                 first_in_time = request.POST.get(f"first_in_{day}")
#                 last_out_time = request.POST.get(f"last_out_{day}")
#
#                 first_in_value = None
#                 last_out_value = None
#
#                 if first_in_time:
#                     naive_dt = datetime.strptime(
#                         f"{attendance_date} {first_in_time}",
#                         "%Y-%m-%d %H:%M"
#                     )
#                     first_in_value = timezone.make_aware(
#                         naive_dt, timezone.get_current_timezone()
#                     )
#
#                 if last_out_time:
#                     naive_dt = datetime.strptime(
#                         f"{attendance_date} {last_out_time}",
#                         "%Y-%m-%d %H:%M"
#                     )
#                     last_out_value = timezone.make_aware(
#                         naive_dt, timezone.get_current_timezone()
#                     )
#
#                 record = Attendance.objects.filter(
#                     staff_id=selected_employee.id,
#                     sch_id=sch_id,
#                     date=attendance_date
#                 ).first()
#
#                 if record:
#
#                     # Apply manual status first
#                     if selected_status:
#                         record.status = selected_status
#
#                     if first_in_value:
#                         record.first_in = first_in_value
#
#                     if last_out_value:
#                         record.last_out = last_out_value
#
#                     # =====================================================
#                     # 🔥 SHIFT RECALCULATION
#                     # =====================================================
#                     if record.first_in and record.last_out:
#
#                         shift = selected_employee.shift
#
#                         if shift:
#
#                             shift_start_naive = datetime.combine(
#                                 attendance_date,
#                                 shift.start_time
#                             )
#
#                             shift_end_naive = datetime.combine(
#                                 attendance_date,
#                                 shift.end_time
#                             )
#
#                             shift_start = timezone.make_aware(
#                                 shift_start_naive,
#                                 timezone.get_current_timezone()
#                             )
#
#                             shift_end = timezone.make_aware(
#                                 shift_end_naive,
#                                 timezone.get_current_timezone()
#                             )
#
#                             # Work Duration
#                             work_duration = record.last_out - record.first_in
#                             record.work_duration = work_duration
#
#                             # Late Calculation
#                             if record.first_in > shift_start:
#                                 late_minutes = int(
#                                     (record.first_in - shift_start).total_seconds() / 60
#                                 )
#                                 record.late = True
#                                 record.late_minutes = late_minutes
#                                 # ✅ Apply late cutoff hour setting
#                                 if payroll_settings and record.first_in.hour >= payroll_settings.late_cutoff_hour:
#                                     record.status = "HALF_DAY"
#
#                             else:
#                                 record.late = False
#                                 record.late_minutes = 0
#
#                             # =====================================================
#                             # 🚫 DO NOT OVERRIDE MANUAL SPECIAL STATUSES
#                             # =====================================================
#
#                             manual_statuses = [
#                                 "CL", "ML", "PERMISSION",
#                                 "WEEKLY_OFF", "HOLIDAY"
#                             ]
#
#                             if record.status not in manual_statuses:
#
#                                 shift_seconds = (shift_end - shift_start).total_seconds()
#                                 worked_seconds = work_duration.total_seconds()
#
#                                 tolerance_seconds = 15 * 60  # 15 min grace
#
#                                 if worked_seconds >= (shift_seconds - tolerance_seconds):
#                                     record.status = "PRESENT"
#                                 elif worked_seconds >= (shift_seconds / 2):
#                                     record.status = "HALF_DAY"
#                                 else:
#                                     record.status = "LOP"
#
#                             # If permission selected → remove late
#                             if record.status == "PERMISSION":
#                                 record.late = False
#                                 record.late_minutes = 0
#
#                     record.save()
#
#                 else:
#                     if selected_status or first_in_value or last_out_value:
#                         Attendance.objects.create(
#                             staff_id=selected_employee.id,
#                             sch_id=sch_id,
#                             date=attendance_date,
#                             status=selected_status if selected_status else "LOP",
#                             first_in=first_in_value,
#                             last_out=last_out_value
#                         )
#
#             return redirect(
#                 f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
#             )
#
#         # =====================================================
#         # ✅ GET SECTION
#         # =====================================================
#
#         records = Attendance.objects.filter(
#             staff_id=employee_id,
#             sch_id=sch_id,
#             date__year=year,
#             date__month=month
#         )
#
#         attendance_dict = {
#             record.date.day: record
#             for record in records
#         }
#
#         for day in range(1, total_days + 1):
#
#             attendance_date = date(year, month, day)
#             record = attendance_dict.get(day)
#
#             status = record.status if record else "LOP"
#
#             if status == "PRESENT":
#                 total_present += 1
#             elif status in ["LOP", "ABSENT"]:
#                 total_absent += 1
#             elif status == "HALF_DAY":
#                 total_half += 1
#             elif status == "MIS_PUNCH":
#                 total_mis += 1
#             elif status in ["CL", "ML", "PERMISSION", "WEEKLY_OFF", "HOLIDAY"]:
#                 total_present += 1
#
#             if record and record.late:
#                 total_late += 1
#
#             attendance_list.append({
#                 "day": day,
#                 "full_date": attendance_date,
#                 "status": status,
#                 "first_in": record.first_in if record else None,
#                 "last_out": record.last_out if record else None,
#                 "work_duration": record.work_duration if record else None,
#                 "punch_count": record.punch_count if record else 0,
#                 "late": record.late if record else False,
#                 "late_minutes": record.late_minutes if record else 0,
#                 "mis_punch": record.mis_punch if record else False,
#             })
#
#     context = {
#         "employees": employees,
#         "selected_employee": selected_employee,
#         "month": month,
#         "year": year,
#         "attendance_list": attendance_list,
#         "status_choices": status_choices,
#         "total_present": total_present,
#         "total_absent": total_absent,
#         "total_half": total_half,
#         "total_late": total_late,
#         "total_mis": total_mis,
#     }
#
#     return render(request, "payroll/monthlyattendance.html", context)

def Staff_Monthly_Attendance(request):

    sch_id = request.session.get('sch_id')
    sdata = get_object_or_404(school, pk=sch_id)

    yr = currentacademicyr.objects.get(school_name=sdata)
    acad_year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    try:
        payroll_settings = sdata.payroll_settings
    except PayrollSettings.DoesNotExist:
        payroll_settings = None

    employees = staff.objects.filter(staff_school=sch_id)

    employee_id = request.GET.get("employee")
    month = int(request.GET.get("month", date.today().month))
    year = int(request.GET.get("year", date.today().year))

    selected_employee = None
    attendance_list = []
    status_choices = Attendance.STATUS_CHOICES

    total_present = 0
    total_absent = 0
    total_half = 0
    total_late = 0
    total_mis = 0

    if employee_id:

        selected_employee = get_object_or_404(staff, id=employee_id)
        total_days = calendar.monthrange(year, month)[1]

        # =====================================================
        # ✅ POST SECTION
        # =====================================================
        if request.method == "POST":

            # =====================================================
            # 🚨 MONTHLY LEAVE VALIDATION (CL / ML / PERMISSION)
            # =====================================================
            if payroll_settings:

                post_cl_count = 0
                post_ml_count = 0
                post_permission_count = 0
                post_permission_minutes = 0

                for d in range(1, total_days + 1):

                    post_status = request.POST.get(f"status_{d}")

                    if post_status == "CL":
                        post_cl_count += 1

                    elif post_status == "ML":
                        post_ml_count += 1

                    elif post_status == "PERMISSION":
                        post_permission_count += 1

                        post_first = request.POST.get(f"first_in_{d}")
                        post_last = request.POST.get(f"last_out_{d}")

                        if post_first and post_last:
                            naive_start = datetime.strptime(
                                f"{date(year, month, d)} {post_first}",
                                "%Y-%m-%d %H:%M"
                            )
                            naive_end = datetime.strptime(
                                f"{date(year, month, d)} {post_last}",
                                "%Y-%m-%d %H:%M"
                            )

                            aware_start = timezone.make_aware(
                                naive_start, timezone.get_current_timezone()
                            )
                            aware_end = timezone.make_aware(
                                naive_end, timezone.get_current_timezone()
                            )

                            minutes = (aware_end - aware_start).total_seconds() / 60
                            post_permission_minutes += minutes

                # 🔹 CL Validation
                if payroll_settings.cl_per_month is not None:
                    if post_cl_count > payroll_settings.cl_per_month:
                        messages.error(
                            request,
                            f"Only {payroll_settings.cl_per_month} Casual Leave allowed per month."
                        )
                        return redirect(
                            f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
                        )

                # 🔹 ML Validation
                if payroll_settings.total_ml is not None:

                    # Count existing ML in this year from DB
                    existing_ml_year = Attendance.objects.filter(
                        staff_id=selected_employee.id,
                        sch_id=sch_id,
                        date__year=year,
                        status="ML"
                    ).count()

                    # Count ML from current POST
                    post_ml_count = 0
                    for d in range(1, total_days + 1):
                        if request.POST.get(f"status_{d}") == "ML":
                            post_ml_count += 1

                    total_ml = post_ml_count  # since month is overwritten fully

                    if total_ml > payroll_settings.total_ml:
                        messages.error(
                            request,
                            f"Only {payroll_settings.total_ml} Medical Leave allowed per year."
                        )
                        return redirect(
                            f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
                        )

                # 🔹 Permission Count Validation
                if payroll_settings.permission_per_month is not None:
                    if post_permission_count > payroll_settings.permission_per_month:
                        messages.error(
                            request,
                            f"Only {payroll_settings.permission_per_month} Permissions allowed per month."
                        )
                        return redirect(
                            f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
                        )

                # 🔹 Permission Hours Validation
                if payroll_settings.permission_per_month:
                    allowed_minutes = payroll_settings.permission_per_month * 60
                    if post_permission_minutes > allowed_minutes:
                        messages.error(
                            request,
                            f"Permission hour limit exceeded. Allowed: {payroll_settings.permission_per_month} hour(s) per month."
                        )
                        return redirect(
                            f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
                        )

            # =====================================================
            # 🔁 YOUR ORIGINAL SAVE LOOP (UNCHANGED)
            # =====================================================
            for day in range(1, total_days + 1):

                attendance_date = date(year, month, day)

                selected_status = request.POST.get(f"status_{day}")
                first_in_time = request.POST.get(f"first_in_{day}")
                last_out_time = request.POST.get(f"last_out_{day}")

                first_in_value = None
                last_out_value = None

                if first_in_time:
                    naive_dt = datetime.strptime(
                        f"{attendance_date} {first_in_time}",
                        "%Y-%m-%d %H:%M"
                    )
                    first_in_value = timezone.make_aware(
                        naive_dt, timezone.get_current_timezone()
                    )

                if last_out_time:
                    naive_dt = datetime.strptime(
                        f"{attendance_date} {last_out_time}",
                        "%Y-%m-%d %H:%M"
                    )
                    last_out_value = timezone.make_aware(
                        naive_dt, timezone.get_current_timezone()
                    )

                record = Attendance.objects.filter(
                    staff_id=selected_employee.id,
                    sch_id=sch_id,
                    date=attendance_date
                ).first()

                if record:

                    if selected_status:
                        record.status = selected_status

                    if first_in_value:
                        record.first_in = first_in_value

                    if last_out_value:
                        record.last_out = last_out_value

                    if record.first_in and record.last_out:

                        shift = selected_employee.shift

                        if shift:

                            shift_start_naive = datetime.combine(
                                attendance_date,
                                shift.start_time
                            )

                            shift_end_naive = datetime.combine(
                                attendance_date,
                                shift.end_time
                            )

                            shift_start = timezone.make_aware(
                                shift_start_naive,
                                timezone.get_current_timezone()
                            )

                            shift_end = timezone.make_aware(
                                shift_end_naive,
                                timezone.get_current_timezone()
                            )

                            work_duration = record.last_out - record.first_in
                            record.work_duration = work_duration

                            if record.first_in > shift_start:
                                late_minutes = int(
                                    (record.first_in - shift_start).total_seconds() / 60
                                )
                                record.late = True
                                record.late_minutes = late_minutes

                                if payroll_settings and record.first_in.hour >= payroll_settings.late_cutoff_hour:
                                    record.status = "HALF_DAY"
                            else:
                                record.late = False
                                record.late_minutes = 0

                            manual_statuses = [
                                "CL", "ML", "PERMISSION",
                                "WEEKLY_OFF", "HOLIDAY"
                            ]

                            if record.status not in manual_statuses:

                                shift_seconds = (shift_end - shift_start).total_seconds()
                                worked_seconds = work_duration.total_seconds()
                                tolerance_seconds = 15 * 60

                                if worked_seconds >= (shift_seconds - tolerance_seconds):
                                    record.status = "PRESENT"
                                elif worked_seconds >= (shift_seconds / 2):
                                    record.status = "HALF_DAY"
                                else:
                                    record.status = "LOP"

                            if record.status == "PERMISSION":
                                record.late = False
                                record.late_minutes = 0

                    record.save()

                else:
                    if selected_status or first_in_value or last_out_value:
                        Attendance.objects.create(
                            staff_id=selected_employee.id,
                            sch_id=sch_id,
                            date=attendance_date,
                            status=selected_status if selected_status else "LOP",
                            first_in=first_in_value,
                            last_out=last_out_value
                        )

            return redirect(
                f"{reverse('Staff_Monthly_Attendance')}?employee={employee_id}&month={month}&year={year}"
            )

        # =====================================================
        # ✅ GET SECTION
        # =====================================================
        records = Attendance.objects.filter(
            staff_id=employee_id,
            sch_id=sch_id,
            date__year=year,
            date__month=month
        )

        attendance_dict = {
            record.date.day: record
            for record in records
        }

        for day in range(1, total_days + 1):

            attendance_date = date(year, month, day)
            record = attendance_dict.get(day)

            status = record.status if record else "LOP"

            if status == "PRESENT":
                total_present += 1
            elif status in ["LOP", "ABSENT"]:
                total_absent += 1
            elif status == "HALF_DAY":
                total_half += 1
            elif status == "MIS_PUNCH":
                total_mis += 1
            elif status in ["CL", "ML", "PERMISSION", "WEEKLY_OFF", "HOLIDAY"]:
                total_present += 1

            if record and record.late:
                total_late += 1

            attendance_list.append({
                "day": day,
                "full_date": attendance_date,
                "status": status,
                "first_in": record.first_in if record else None,
                "last_out": record.last_out if record else None,
                "work_duration": record.work_duration if record else None,
                "punch_count": record.punch_count if record else 0,
                "late": record.late if record else False,
                "late_minutes": record.late_minutes if record else 0,
                "mis_punch": record.mis_punch if record else False,
            })

    context = {
        "employees": employees,
        "selected_employee": selected_employee,
        "month": month,
        "year": year,
        "attendance_list": attendance_list,
        "status_choices": status_choices,
        "total_present": total_present,
        "total_absent": total_absent,
        "total_half": total_half,
        "total_late": total_late,
        "total_mis": total_mis,
    }

    return render(request, "payroll/monthlyattendance.html", context)

def staff_monthly_summary(request):

    sch_id = request.session.get("sch_id")
    sdata = get_object_or_404(school, pk=sch_id)

    # Get Payroll Settings
    try:
        payroll_settings = sdata.payroll_settings
    except PayrollSettings.DoesNotExist:
        payroll_settings = None

    month = request.GET.get("month")
    year = request.GET.get("year")

    summary_data = []
    months = [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    if month and year:
        month = int(month)
        year = int(year)

        total_days = calendar.monthrange(year, month)[1]
        employees = staff.objects.filter(staff_school=sch_id)

        for emp in employees:

            records = Attendance.objects.filter(
                staff_id=emp.id,
                sch_id=sch_id,
                date__year=year,
                date__month=month
            )

            present = records.filter(status="PRESENT").count()
            half_day = records.filter(status="HALF_DAY").count()
            cl = records.filter(status="CL").count()
            ml = records.filter(status="ML").count()
            permission = records.filter(status="PERMISSION").count()
            lop = records.filter(status__in=["LOP", "ABSENT"]).count()
            weekly_off = records.filter(remarks="Weekly-OFF").count()
            holiday = records.filter(remarks="Special-OFF").count()
            mispunch = records.filter(status="MIS_PUNCH").count()
            late = records.filter(late=True).count()

            # --------------------------------------------------
            # WORKING DAYS
            # --------------------------------------------------
            working_days = total_days - weekly_off - holiday

            total_lop_days = lop

            if payroll_settings:

                # -------------------------
                # HALF DAY CALCULATION
                # -------------------------
                half_day_lop = half_day * 0.5

                # -------------------------
                # LATE CALCULATION
                # -------------------------
                grace = payroll_settings.grace_late_count
                lop_after_grace = float(payroll_settings.lop_after_grace)

                remaining_late = max(late - grace, 0)
                late_lop = remaining_late * lop_after_grace

                # -------------------------
                # TOTAL LOP
                # -------------------------
                total_lop_days = lop + half_day_lop + late_lop

            # --------------------------------------------------
            # SALARY DAYS
            # --------------------------------------------------
            salary_days = total_days - total_lop_days

            if salary_days < 0:
                salary_days = 0

            summary_data.append({
                "employee": emp,
                "present": present,
                "half_day": half_day,
                "cl": cl,
                "ml": ml,
                "permission": permission,
                "lop": lop,
                "weekly_off": weekly_off,
                "holiday": holiday,
                "mispunch": mispunch,
                "late": late,
                "working_days": working_days,
                "total_lop_days": round(total_lop_days, 2),
                "salary_days": round(salary_days, 2),
                "total_days": total_days
            })

    context = {
        "summary_data": summary_data,
        "months": months,
        "selected_month": int(month) if month else "",
        "selected_year": int(year) if year else date.today().year
    }

    return render(request, "payroll/monthly_summary.html", context)

@transaction.atomic
def generate_payroll(request):

    if request.method != "POST":
        return redirect("staff_monthly_summary")

    sch_id = request.session.get("sch_id")
    sdata = get_object_or_404(school, pk=sch_id)

    month = int(request.POST.get("month"))
    year = int(request.POST.get("year"))

    payroll_employees = PayrollEmployee.objects.filter(
        school=sdata,
        employee_id__status='Active'
    )

    for emp in payroll_employees:

        # --------------------------------------
        # FETCH ATTENDANCE
        # --------------------------------------
        records = Attendance.objects.filter(
            staff=emp.staff,
            sch_id=sch_id,
            date__year=year,
            date__month=month
        )

        lop = records.filter(status__in=["LOP", "ABSENT"]).count()
        half_day = records.filter(status="HALF_DAY").count()
        late = records.filter(late=True).count()

        # --------------------------------------
        # LOP CALCULATION
        # --------------------------------------
        total_lop_days = Decimal(lop) + (Decimal(half_day) * Decimal('0.5'))

        # (Optional: Late logic can be added later)

        # --------------------------------------
        # SALARY CALCULATION (Fixed 30 Days)
        # --------------------------------------
        gross = emp.gross_salary

        basic = gross * (emp.basic_percentage / Decimal('100'))
        hra = gross * (emp.hra_percentage / Decimal('100'))

        per_day = gross / Decimal('30')
        lop_amount = per_day * total_lop_days

        net_salary = gross - lop_amount

        # --------------------------------------
        # CHECK IF FINALIZED
        # --------------------------------------
        existing = PayrollMonthly.objects.filter(
            payroll_employee=emp,
            month=month,
            year=year
        ).first()

        if existing and existing.is_finalized:
            continue  # Skip finalized payroll

        # --------------------------------------
        # CREATE OR UPDATE
        # --------------------------------------
        PayrollMonthly.objects.update_or_create(
            payroll_employee=emp,
            month=month,
            year=year,
            defaults={
                "school": sdata,
                "total_lop_days": total_lop_days,
                "gross_salary": gross,
                "basic_da": basic,
                "hra": hra,
                "net_salary": net_salary,
            }
        )

    messages.success(request, "Payroll Generated Successfully")
    return redirect(
        f"{reverse('Staff_Monthly_Summary')}?employee={employee_id}&month={month}&year={year}"
    )


def payroll_register(request):

    sch_id = request.session.get("sch_id")
    sdata = get_object_or_404(school, pk=sch_id)

    month = request.GET.get("month")
    year = request.GET.get("year")

    payrolls = None
    total_gross = Decimal('0.00')
    total_net = Decimal('0.00')
    total_lop = Decimal('0.00')

    if month and year:
        month = int(month)
        year = int(year)

        payrolls = PayrollMonthly.objects.filter(
            school=sdata,
            month=month,
            year=year
        ).select_related("payroll_employee", "payroll_employee__staff")

        totals = payrolls.aggregate(
            gross_sum=Sum("gross_salary"),
            net_sum=Sum("net_salary"),
            lop_sum=Sum("total_lop_days")
        )

        total_gross = totals["gross_sum"] or Decimal('0.00')
        total_net = totals["net_sum"] or Decimal('0.00')
        total_lop = totals["lop_sum"] or Decimal('0.00')

    context = {
        "payrolls": payrolls,
        "month": month,
        "year": year,
        "total_gross": total_gross,
        "total_net": total_net,
        "total_lop": total_lop,
    }

    return render(request, "payroll/payroll_register.html", context)


def PayrollSet(request):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        messages.error(request, "School session not found.")
        return redirect('dashboard')

    # ✅ Get School
    sdata = get_object_or_404(school, pk=sch_id)

    # ✅ Get Academic Year
    yr = get_object_or_404(currentacademicyr, school_name=sdata)
    year = get_object_or_404(academicyr, acad_year=yr, school_name=sdata)

    # ✅ Since OneToOne → use first() (safe if not created yet)
    payroll_settings = PayrollSettings.objects.filter(school=sdata).first()

    context = {
        'skool': sdata,
        'year': year,
        'payroll': payroll_settings
    }

    return render(request, 'payroll/psettings.html', context)

def create_payroll_settings(request):

    # ✅ Get School from session
    sch_id = request.session.get('sch_id')
    if not sch_id:
        messages.error(request, "School not found in session.")
        return redirect("login")

    sdata = get_object_or_404(school, pk=sch_id)

    # ✅ Get Current Academic Year
    yr = currentacademicyr.objects.get(school_name=sdata)
    acad_year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # ✅ Check if PayrollSettings already exists for this school & year
    payroll_instance = PayrollSettings.objects.filter(
        school=sdata
    ).first()

    # =====================================================
    # POST METHOD
    # =====================================================
    if request.method == "POST":

        if payroll_instance:
            # Update existing settings
            form = PayrollSettingsForm(request.POST, instance=payroll_instance)
        else:
            # Create new settings
            form = PayrollSettingsForm(request.POST)

        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.school = sdata
            payroll.academic_year = acad_year
            payroll.save()

            messages.success(request, "Payroll settings saved successfully.")
            return redirect("psettings")

        else:
            messages.error(request, "Please correct the errors below.")

    # =====================================================
    # GET METHOD
    # =====================================================
    else:
        if payroll_instance:
            form = PayrollSettingsForm(instance=payroll_instance)
        else:
            form = PayrollSettingsForm()

    context = {
        "form": form,
        "payroll_instance": payroll_instance
    }

    return render(request, "payroll/create_psettings.html", context)

def edit_payroll_settings(request):
    sch_id = request.session.get('sch_id')

    if not sch_id:
        messages.error(request, "School session not found.")
        return redirect('dashboard')

    sdata = get_object_or_404(school, pk=sch_id)

    # ✅ Since OneToOne, get that school's settings
    payroll = get_object_or_404(PayrollSettings, school=sdata)

    if request.method == "POST":
        form = PayrollSettingsForm(request.POST, instance=payroll)

        if form.is_valid():
            form.save()
            messages.success(request, "Payroll Settings updated successfully.")
            return redirect('psettings')
    else:
        form = PayrollSettingsForm(instance=payroll)

    return render(request, 'payroll/edit_psettings.html', {
        'form': form,
        'skool': sdata
    })

def delete_payroll_settings(request):
    sch_id = request.session.get('sch_id')



    sdata = get_object_or_404(school, pk=sch_id)

    # ✅ Ensure payroll settings belongs to this school
    data = get_object_or_404(PayrollSettings,school=sdata)

    if request.method == "POST":
        data.delete()
        messages.success(request, "Payroll Settings Deleted Successfully.")
        return redirect('psettings')

    messages.error(request, "Invalid request.")
    return redirect('psettings')


def Holiday_List(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Holiday.objects.filter(sch=sdata)
    return render(request,'payroll/holidays.html',context={'skool':sdata,'year':year,'data':data})


@transaction.atomic
def add_holiday(request):
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return render(request, "error.html", {"message": "School not found in session"})

    sdata = get_object_or_404(school, pk=sch_id)

    yr = currentacademicyr.objects.get(school_name=sdata)
    acad_year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    initial_data = {'sch': sdata}

    if request.method == 'POST':
        form = add_holidayform(request.POST)

        if form.is_valid():
            holiday = form.save()

            holiday_date = holiday.date   # Make sure this matches your Holiday model field name
            sts = holiday.name
            # 🔥 Get all staff in this school
            all_staff = staff.objects.filter(staff_school=sdata)

            for emp in all_staff:
                attendance_obj, created = Attendance.objects.get_or_create(
                    sch=sdata,
                    staff=emp,
                    date=holiday_date,

                    defaults={
                        "status": sts,
                        "is_manual": True,
                        "remarks": sts
                    }

                )


                # If already exists → Update it
                if not created:
                    attendance_obj.status = sts
                    attendance_obj.is_manual = True
                    attendance_obj.remarks = sts
                    attendance_obj.save()

            messages.success(request, "Holiday Added & Attendance Updated Successfully")
            return redirect('Holidays')

    else:
        form = add_holidayform(initial=initial_data)

    return render(
        request,
        'payroll/add_holiday.html',
        context={
            'form': form,
            'skool': sdata,
            'year': acad_year
        }
    )

@transaction.atomic
def delete_holiday(request,id):

    sch_id = request.session.get('sch_id')
    if not sch_id:
        return render(request, "error.html", {"message": "School not found in session"})

    sdata = get_object_or_404(school, pk=sch_id)

    holiday = get_object_or_404(Holiday, id=id, sch=sdata)

    holiday_date = holiday.date

    # 🔥 Get all attendance records marked as HOLIDAY for this date
    attendance_records = Attendance.objects.filter(
        sch=sdata,
        date=holiday_date,
        status="HOLIDAY"
    )

    for record in attendance_records:

        # If it was manually marked as holiday by system
        if record.is_manual:
            # Either delete or revert
            record.delete()  # 🔥 Clean remove

        else:
            # If somehow not manual, revert to LOP
            record.status = "LOP"
            record.save()

    # Now delete holiday
    holiday.delete()

    messages.success(request, "Holiday Deleted & Attendance Reverted Successfully")

    return redirect('Holidays')


@transaction.atomic
def reapply_holidays_attendance(request):

    sch_id = request.session.get('sch_id')
    if not sch_id:
        return render(request, "error.html", {"message": "School not found in session"})

    sdata = get_object_or_404(school, pk=sch_id)

    # Academic Year
    yr = currentacademicyr.objects.get(school_name=sdata)
    acad_year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # Get all holidays for this school
    holidays = Holiday.objects.filter(
        sch=sdata,

    )

    # Get all staff
    all_staff = staff.objects.filter(staff_school=sdata)

    total_created = 0
    total_updated = 0

    for holiday in holidays:

        holiday_date = holiday.date
        holiday_status = holiday.name  # Example: HOLIDAY

        for emp in all_staff:

            attendance_obj, created = Attendance.objects.get_or_create(
                sch=sdata,
                staff=emp,
                date=holiday_date,
                defaults={
                    "status": holiday_status,
                    "is_manual": True,
                    "remarks": holiday_status
                }
            )

            if created:
                total_created += 1
            else:
                # If attendance exists but not holiday → update
                if attendance_obj.status != holiday_status:
                    attendance_obj.status = holiday_status
                    attendance_obj.is_manual = True
                    attendance_obj.remarks = holiday_status
                    attendance_obj.save()
                    total_updated += 1

    messages.success(
        request,
        f"Holidays Reapplied Successfully. Created: {total_created}, Updated: {total_updated}"
    )

    return redirect('Holidays')