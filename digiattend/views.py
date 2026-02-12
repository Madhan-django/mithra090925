from django.shortcuts import render,redirect,HttpResponse
from .forms import AttendanceDateForm,NewBioDeviceForm,BioShiftForm,BioDeptForm,EmployeeForm
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from django.db.models import Min, Max
# Create your views here.

from .models import BiometricLog,Employee,BioDevices,DeviceList,BioDept,get_biometric_table_for_month



def BioDeviceList(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = BioDevices.objects.filter(BioSchool=sdata)
    return render(request,'biometrics/Devices.html',context={'data':data})

def NewBioDevices(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
        'BioSchool':sdata
    }
    if request.method == 'POST':
        form = NewBioDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New Device has been Added Successfully')
    form =NewBioDeviceForm(initial=initial_data)
    return render(request,'biometrics/NewDevice.html',context={'form':form})

def BioDeviceDelete(request,Biodev_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = BioDevices.objects.get(id=Biodev_id)
    data.delete()
    messages.success(request," The Device deleted Successfully")
    return redirect('DeviceList')

def NewShift(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
        'ShiftSchool':sdata
    }
    if request.method == 'POST':
        form = BioShiftForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New Shift has been Added Successfully')
    form =BioShiftForm(initial=initial_data)
    return render(request,'biometrics/NewDevice.html',context={'form':form})

def NewDept(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
        'DeptSchool':sdata
    }
    if request.method == 'POST':
        form = BioDeptForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New Department has been Added Successfully')
        else:
            return HttpResponse("form Invalid")
    form =BioDeptForm(initial=initial_data)
    return render(request,'biometrics/NewDevice.html',context={'form':form})


def log_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    device_data = DeviceList.objects.all()
    attendance_records = []  # List to store the attendance data
    form = AttendanceDateForm()

    if request.method == 'POST':
        try:
            form = AttendanceDateForm(request.POST)
            if form.is_valid():
                SchBio = BioDevices.objects.filter(BioSchool=sdata)

                if SchBio.exists():
                    selected_date = form.cleaned_data['date']
                    start_of_day = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()))
                    end_of_day = timezone.make_aware(datetime.combine(selected_date, datetime.max.time()))
                    # **Dynamic Table Handling:**
                    # Get the correct table name for the selected date
                    table_name = get_biometric_table_for_month(selected_date)
                    # Set the table name dynamically
                    BiometricLog.set_table_name(table_name)
                    emps = Employee.objects.filter(EmpSchool=sdata, Status="Working")

                    for bio in SchBio:
                        for Dev in device_data:
                            if bio.BioSerial == Dev.SerialNumber:
                                for emp in emps:
                                    # Filter biometric logs for each employee on the selected device
                                    data = BiometricLog.objects.filter(
                                        LogDate__range=(start_of_day, end_of_day),
                                        DeviceId=Dev.DeviceId,
                                        UserId=emp.EmployeeCode
                                    )

                                    if data.exists():
                                        # Get the first punch (earliest)
                                        first_log = data.earliest('LogDate')
                                        first_punch = first_log.LogDate
                                        last_log = data.latest('LogDate')
                                        last_punch = last_log.LogDate
                                        duration = last_log.LogDate - first_log.LogDate
                                        # Get the department's shift timings
                                        shift_start_time = emp.Dept.ShiftDet.ShiftStartTime
                                        shift_start_datetime = timezone.make_aware(
                                            datetime.combine(selected_date, shift_start_time))

                                        shift_End_time = emp.Dept.ShiftDet.ShiftEndTime
                                        shift_End_datetime = timezone.make_aware(
                                            datetime.combine(selected_date, shift_End_time))

                                        # Check if the first punch is early or late
                                        if first_punch <= shift_start_datetime:
                                            early_by = (
                                                                   shift_start_datetime - first_punch).total_seconds() // 60  # Minutes early
                                            late_by = None  # Not late
                                        else:
                                            late_by = (
                                                                  first_punch - shift_start_datetime).total_seconds() // 60  # Minutes late
                                            early_by = None  # Not early

                                        if last_punch <= shift_End_datetime:
                                            early_out = (
                                                                    shift_End_datetime - last_punch).total_seconds() // 60  # Minutes early
                                            late_out = None  # Not late
                                        else:
                                            late_out = (
                                                                   last_punch - shift_End_datetime).total_seconds() // 60  # Minutes late
                                            early_out = None  # Not early
                                        print("Early/late", early_out, late_out)
                                        # Create a dictionary for the current employee's attendance record
                                        attendance_record = {
                                            'employee_name': emp.EmployeeName_id,
                                            'first_punch': first_punch,
                                            'early_by': early_by,
                                            'late_by': late_by,
                                            'last_punch': last_punch,
                                            'early_out': early_out,
                                            'late_out': late_out,
                                            'Duration': duration,
                                            'department': emp.Dept.DeptName,
                                            'shift_name': emp.Dept.ShiftDet.ShiftName,
                                            'shift_timings': f"{emp.Dept.ShiftDet.ShiftStartTime} - {emp.Dept.ShiftDet.ShiftEndTime}"
                                        }

                                        # Add the record to the attendance list
                                        attendance_records.append(attendance_record)
                                    else:
                                        # Handle the case where the employee has no punch data for the day
                                        attendance_record = {
                                            'employee_name': emp.EmployeeName_id,
                                            'first_punch': 'ABS',
                                            'early_by': None,
                                            'late_by': None,
                                            'last_punch': 'ABS',
                                            'department': emp.Dept.DeptName,
                                            'shift_name': emp.Dept.ShiftDet.ShiftName,
                                            'shift_timings': f"{emp.Dept.ShiftDet.ShiftStartTime} - {emp.Dept.ShiftDet.ShiftEndTime}"
                                        }
                                        attendance_records.append(attendance_record)

                    return render(request, 'biometrics/log_list.html', {'attendance_records': attendance_records})
                else:
                    messages.info(request, "Biometrics Not Configured. Please Contact Support")
        except Exception as e:
            error = f'{e}'
            return HttpResponse(error)


    return render(request, 'biometrics/attendanceform.html', context={'form': form})

def employeelist(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Employee.objects.filter(EmpSchool=sdata,Status='Working')
    return render(request,'biometrics/employeelist.html',context={'data':data})

def employeeUpdate(request,emp_id):
    employee = Employee.objects.get(EmployeeCode = emp_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # Save the updated employee data
            return redirect('employeelist')  # Redirect to the employee list or a success page

    form = EmployeeForm(instance=employee)
    return render(request, 'biometrics/update_employee.html', {'form': form, 'employee': employee})

def NewEmployee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()  # Save the updated employee data
            return redirect('employeelist')  # Redirect to the employee list or a success page

    form = EmployeeForm()
    return render(request, 'biometrics/update_employee.html', {'form': form})
