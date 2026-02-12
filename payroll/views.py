from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import JsonResponse
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Department,Designation,PayrollEmployee,PayrollBank,Allowance,Deduction,Employee_allowance_Details,Employee_deduction_Details,Loan
from django.contrib import messages
from .forms import add_deptform,add_desgform,PayrollEmployeeForm,PayrollBankForm,PayrollBankFormSet,payrollBankFormupdate,Allowanceform,Deductionform,NewLoanForm
import math
from dateutil.relativedelta import relativedelta
from django.db import connection
from datetime import datetime, time, timedelta
from django.utils import timezone
from openpyxl import Workbook

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



# Attendance Rules
LATE_AFTER_TIME = time(9, 0, 0)          # 9:00 AM
MIN_WORK_HOURS = timedelta(hours=8)      # 8 hours


def daily_attendance_view(request):
    selected_date = request.GET.get('date')
    export = request.GET.get('export')   # 👈 check export parameter
    attendance_list = []
    rows = []

    if selected_date:
        date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
        table_name = f"devicelogs_{date_obj.month}_{date_obj.year}"

        query = f"""
            SELECT
                UserId,
                MIN(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS in_time,
                MAX(CONVERT_TZ(LogDate, '+00:00', '+05:30')) AS out_time,
                COUNT(*) as punch_count
            FROM {table_name}
            WHERE DATE(CONVERT_TZ(LogDate, '+00:00', '+05:30')) = %s
            GROUP BY UserId
            ORDER BY UserId
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [selected_date])
            rows = cursor.fetchall()

        for row in rows:
            user_id, in_time, out_time, punch_count = row

            status = "PRESENT"
            late = False
            mispunch = False
            work_hours = ""

            if punch_count == 1:
                mispunch = True
                status = "MIS PUNCH"

            elif in_time and out_time:
                work_duration = out_time - in_time

                total_seconds = int(work_duration.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                work_hours = f"{hours:02}:{minutes:02}:{seconds:02}"

                if in_time.time() > LATE_AFTER_TIME:
                    late = True

                if work_duration < MIN_WORK_HOURS:
                    status = "HALF DAY"

            attendance_list.append({
                "user_id": user_id,
                "in_time": in_time,
                "out_time": out_time,
                "work_hours": work_hours,
                "late": late,
                "mispunch": mispunch,
                "status": status,
                "punch_count": punch_count
            })

    # ✅ EXPORT TO EXCEL
    if export == "excel" and selected_date:
        wb = Workbook()
        ws = wb.active
        ws.title = "Daily Attendance"

        headers = [
            "User ID",
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
        "selected_date": selected_date
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
