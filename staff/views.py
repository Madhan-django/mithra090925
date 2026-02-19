from django.shortcuts import render,redirect,HttpResponse
from django.utils import timezone
from .models import staff,staff_attendance,staff_attendancegen,homework,temp_homework,Dept,Shift
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,subjects
from .forms import add_staff_form,add_staff_attendance_gen,add_homework_form,edit_homework_form,add_deptfm,add_shiftform
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from django_q.models import Schedule
from django.utils.timezone import now
from django.contrib.auth.models import User,Group
from authenticate.decorators import allowed_users
from django.contrib.auth.forms import PasswordChangeForm
from .utils import render_to_pdf
import csv



# Create your views here.

def Dept_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Dept.objects.filter(sch=sdata)
    return render(request, 'staff/DeptList.html', context={'data': data, 'skool': sdata, 'year': year})

def Dept_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'sch':sdata
    }
    if request.method == 'POST':
        form  = add_deptfm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department Added successfully")
            return redirect('dept')
    else:
        form = add_deptfm(initial=initial_data)
    return render(request,'staff/add_dept.html',context={'form':form,'skool':sdata,'year':year})

def Dept_update(request,dept_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Dept.objects.get(id=dept_id)
    if request.method == 'POST':
        form = add_deptfm(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully")
            return redirect('dept')
    else:
        form  = add_deptfm(instance = data)
    return render(request,'staff/add_dept.html',context={'form':form,'skool':sdata,'year':year})

def Dept_del(request,dept_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Department.objects.get(id=dept_id)
    data.delete()
    messages.success(request,"Department deleted successfully")
    return redirect('dept')

def shifts(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Shift.objects.filter(sch=sdata)
    return render(request, 'staff/shifts.html', context={'data': data, 'skool': sdata, 'year': year})

def shift_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'sch':sdata
    }
    if request.method == 'POST':
        form  = add_shiftform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift Added successfully")
            return redirect('shifts')
    else:
        form = add_shiftform(initial=initial_data)
    return render(request,'staff/add_shift.html',context={'form':form,'skool':sdata,'year':year})

def shift_update(request,shift_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Shift.objects.get(id=shift_id)
    if request.method == 'POST':
        form = add_shiftform(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift updated successfully")
            return redirect('shifts')
    else:
        form  = add_shiftform(instance = data)
    return render(request,'staff/update_shift.html',context={'form':form,'skool':sdata,'year':year})

def shift_del(request,shift_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Shift.objects.get(id=shift_id)
    data.delete()
    messages.success(request,"Shift deleted successfully")
    return redirect('shifts')



@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def stafflist(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = staff.objects.filter(staff_school=sdata,status='Active')
    paginator = Paginator(data,30)  # Show 30 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    return render(request,'staff/stafflist.html',context={'data': page_obj, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_staff(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    form = add_staff_form(initial={
        'staff_school': sdata,
    })

    if request.method == 'POST':
        form = add_staff_form(request.POST, request.FILES)
        if form.is_valid():
            # Create the username
            name_str = request.POST['first_name']
            date_str1 = request.POST['dob']
            grp = request.POST['permission_group']
            eml = request.POST['email']

            name_str = name_str[0:3]
            dtyr = date_str1[0:4]
            dtmon = date_str1[5:7]
            dt = date_str1[8:10]
            usernm = name_str + dt + dtmon + dtyr

            # Create the Django user
            ruser = User.objects.create_user(
                username=usernm,
                email=eml,
                password='Welcome@123'
            )

            # Add to group
            group = Group.objects.get(name='Teacher')
            ruser.groups.add(group)

            # Save staff object with the new user
            chgusernm = form.save(commit=False)
            chgusernm.staff_user = ruser
            chgusernm.save()

            messages.success(request, 'Staff has been added successfully')
            return redirect('stafflist')
        else:
            return HttpResponse(form.errors)

    return render(request, 'staff/add_staff.html', context={'form': form, 'skool': sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_update(request, staff_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = staff.objects.get(pk=staff_id)
    form = add_staff_form(instance=data)
    if request.method=='POST':
        form = add_staff_form(request.POST or None, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,' Staff Record Updated Successfully')
            return redirect('stafflist')
        else:
            return HttpResponse(str(form.errors))
    context ={'form':form,'skool':sdata,'year':year}
    return render(request,'staff/update_staff.html',context)


@allowed_users(allowed_roles=['superadmin','Admin'])
def staff_delete(request,staff_id):
    data = staff.objects.get(pk=staff_id)
    usr = User.objects.get(username=data.staff_user)
    data.delete()
    usr.delete()
    messages.success(request,'Staff Deleted Successfully')
    return redirect('stafflist')

@allowed_users(allowed_roles=['superadmin','Admin'])
def staff_status(request,staff_id):
    data = staff.objects.get(pk=staff_id)
    data.status='In-Active'
    data.save()
    messages.success(request,'Staff Exitted successfully')
    return redirect('stafflist')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_csv(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staff.csv"'
    writer = csv.writer(response)
    writer.writerow( [sdata,])
    writer.writerow(['First Name','Last_name','Gender','DOB','Address','Mobile','Email','Date of Joining','Role','Salary','Designation','Qualification','Status','User ID',])
    staff_data= staff.objects.filter(staff_school=sdata)
    for obj in staff_data:
        writer.writerow([obj.first_name,obj.last_name,obj.gender,obj.dob, obj.address,obj.mobile,obj.email,obj.join,obj.role,
                         obj.salary,obj.desg,obj.qualification,obj.status,obj.staff_user,])

    return response

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def print_staff(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = staff.objects.filter(staff_school=sdata)
    data={
        'rec_data':rec_data,
        'sch_name':sdata
    }

    pdf = render_to_pdf('staff/staff_print.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def gen_staff_attendance(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    initial_data = {
        'staff_school': sdata
    }
    form = add_staff_attendance_gen(initial=initial_data)
    if request.method == "POST":
        form = add_staff_attendance_gen(request.POST)
        if form.is_valid():
          ddate= form.cleaned_data['attndate']
          print('entered ddate')
          if staff_attendance.objects.filter(attndate=ddate,staff_school=sdata).exists():
              messages.info(request,'Attendance already Updated')
              data = staff_attendance.objects.filter(attndate=ddate,staff_school=sdata)
              return render(request, 'staff/add_staff_attendance.html', context={'data': data, 'skool': sdata,'form':form})
          else:
              staffs = staff.objects.filter(staff_school=sch_id)
              for stf in staffs:
                  staff_attendance.objects.create(attndate=ddate,staff_name=stf,status='Present',staff_school=sdata)
                  data = staff_attendance.objects.filter(attndate=ddate, staff_school=sdata)
              return render(request,'staff/add_staff_attendance.html',context={'data':data,'skool':sdata,'form':form})
    return render(request,'staff/add_staff_attendance.html',context={'form':form,'skool':sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_absent(request,attn_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    initial_data = {
        'staff_school': sdata
    }
    form = add_staff_attendance_gen(initial=initial_data)
    staffs = staff_attendance.objects.get(id=attn_id)
    staffs.status='Absent'
    staffs.save()
    data= staff_attendance.objects.filter(attndate=staffs.attndate,staff_school=staffs.staff_school)
    if request.method == "POST":
        form = add_staff_attendance_gen(request.POST)
        if form.is_valid():
          ddate= form.cleaned_data['attndate']
          print('entered ddate')
          if staff_attendance.objects.filter(attndate=ddate,staff_school=sdata).exists():
              messages.info(request,'Attendance already Updated')
              data = staff_attendance.objects.filter(attndate=ddate,staff_school=sdata)
              return render(request, 'staff/add_staff_attendance.html', context={'data': data, 'skool': sdata,'form':form})
          else:
              staffs = staff.objects.filter(staff_school=sch_id)
              for stf in staffs:
                  staff_attendance.objects.create(attndate=ddate,staff_name=stf,status='Present',staff_school=sdata)
                  data = staff_attendance.objects.filter(attndate=ddate, staff_school=sdata)
              return render(request,'staff/add_staff_attendance.html',context={'data':data,'skool':sdata,'form':form})
    return render(request, 'staff/add_staff_attendance.html', context={'data': data, 'skool': sdata, 'form': form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_present(request,attn_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    initial_data = {
        'staff_school': sdata
    }
    form = add_staff_attendance_gen(initial=initial_data)
    staffs = staff_attendance.objects.get(id=attn_id)
    staffs.status='Present'
    staffs.save()
    data= staff_attendance.objects.filter(attndate=staffs.attndate,staff_school=staffs.staff_school)
    if request.method == "POST":
        form = add_staff_attendance_gen(request.POST)
        if form.is_valid():
          ddate= form.cleaned_data['attndate']
          print('entered ddate')
          if staff_attendance.objects.filter(attndate=ddate,staff_school=sdata).exists():
              messages.info(request,'Attendance already Updated')
              data = staff_attendance.objects.filter(attndate=ddate,staff_school=sdata)
              return render(request, 'staff/add_staff_attendance.html', context={'data': data, 'skool': sdata,'form':form})
          else:
              staffs = staff.objects.filter(staff_school=sch_id)
              for stf in staffs:
                  staff_attendance.objects.create(attndate=ddate,staff_name=stf,status='Present',staff_school=sdata)
                  data = staff_attendance.objects.filter(attndate=ddate, staff_school=sdata)
              return render(request,'staff/add_staff_attendance.html',context={'data':data,'skool':sdata,'form':form})
    return render(request, 'staff/add_staff_attendance.html', context={'data': data, 'skool': sdata, 'form': form})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_viewattendance(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    initial_data = {
        'staff_school': sdata
    }
    form = add_staff_attendance_gen(initial=initial_data)
    if request.method == 'POST':
        form = add_staff_attendance_gen(request.POST)
        if form.is_valid():
            ddate = form.cleaned_data['attndate']
            if staff_attendance.objects.filter(attndate=ddate,staff_school=sdata).exists():
                data = staff_attendance.objects.filter(attndate=ddate,staff_school=sdata)
                return render(request,'staff/viewattendance.html',context={'data':data,'form':form,'skool':sdata})
            else:
                messages.info(request,"Attendance Not Available")
                return redirect('staff_viewattendance')
    return render(request,'staff/viewattendance.html',context={'form':form,'skool':sdata})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts', 'Teacher'])
def add_homeworks(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    hclass = sclass.objects.filter(school_name=sdata)
    user = request.user.id
    usr = User.objects.get(id=user)
    
    initial_data = {
        'acad_yr': yr,
        'school_homework': sdata,
        'created_by': usr.id
    }
    
    if request.method == 'POST':
        
        form = add_homework_form(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save()
            rec_id = instance.id

            # Schedule daily task at 6:00 PM
            today_6pm = now().replace(hour=18, minute=0, second=0, microsecond=0)
            if now() > today_6pm:
                today_6pm += timedelta(days=1)
                      
            Schedule.objects.create(
                func='staff.tasks.send_homework',  # Adjust this if your task path is different
                schedule_type=Schedule.DAILY,
                next_run= next_run_time,
                args=[rec_id],
                name=f"Send Homework Daily [{rec_id}]"  # Optional but helpful for tracking
            )

            messages.success(request, 'Homework Added and Scheduled Successfully')
            return redirect('homework')

        else:
            messages.info(request, 'Invalid Data')
            return redirect('homework')

    else:
        form = add_homework_form(initial=initial_data)

    return render(request, 'staff/add_homework.html', {
        'form': form,
        'hclass': hclass,
        'skool': sdata,
        'usr': usr
    })

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts', 'Teacher'])
def add_homeworks(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    hclass = sclass.objects.filter(school_name=sdata)
    user = request.user.id
    usr = User.objects.get(id=user)

    initial_data = {
        'acad_yr': yr,
        'school_homework': sdata,
        'created_by': usr.id
    }

    if request.method == 'POST':
        form = add_homework_form(request.POST,request.FILES, initial=initial_data)
        if form.is_valid():
            instance = form.save()
            rec_id = instance.id

            #Schedule daily task at 6:00 PM
            today_6pm = now().replace(hour=18, minute=0, second=0, microsecond=0)
            
            #now_plus_1min = timezone.now() + timedelta(minutes=1)
            Schedule.objects.create(
                func='staff.tasks.send_homework',  # Adjust this if your task path is different
                schedule_type=Schedule.ONCE,
                next_run= today_6pm,
                args=[rec_id],
                name=f"Send Homework Daily [{rec_id}]"  # Optional but helpful for tracking
            )

            messages.success(request, 'Homework Added and Scheduled Successfully')
            return redirect('homework')

        else:
            messages.info(request, 'Invalid Data')
            return redirect('homework')

    else:
        form = add_homework_form(initial=initial_data)

    return render(request, 'staff/add_homework.html', {
        'form': form,
        'hclass': hclass,
        'skool': sdata,
        'usr': usr
    })
    
    
@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts', 'Teacher'])
def add_homework(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    hclass = sclass.objects.filter(school_name=sdata)
    user = request.user.id
    usr = User.objects.get(id=user)
    try:
        stf = staff.objects.get(staff_user=usr)
    except:
        stf = staff.objects.get(id=1)

    initial_data = {
        'acad_yr': yr,
        'school_homework': sdata,
        'created_by': stf
    }

    if request.method == 'POST':
        form = add_homework_form(request.POST,request.FILES, initial=initial_data)
        if form.is_valid():
            instance = form.save()
            messages.success(request, 'Homework Added and Scheduled Successfully')
            return redirect('homework')

        else:
            err = str(form.errors)
            return HttpResponse(err)

    else:
        form = add_homework_form(initial=initial_data)

    return render(request, 'staff/add_homework.html', {
        'form': form,
        'hclass': hclass,
        'skool': sdata,
        'usr': stf
    })

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def homework_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    today = now().date()
    seven_days_ago = today - timedelta(days=7)

    data = temp_homework.objects.filter(
        school_homework=sdata,
        homework_date__gte=seven_days_ago   # change 'date' to your actual field name
    ).order_by('-id')

    return render(request, 'staff/homework.html',
                  context={'data': data, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_homework(request,homework_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = temp_homework.objects.get(pk=homework_id)


    if request.method == 'POST':
        form = edit_homework_form(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homework Updated Successfully')
            return redirect('homework')
    form = edit_homework_form(instance=data)

    return render(request, 'staff/update_homework.html', context= {'form': form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin'])
def delete_homework(request,homework_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = temp_homework.objects.get(pk=homework_id)
    data.delete()
    messages.success(request,'Homework Deleted Successfully')
    return redirect('homework')
    
@allowed_users(allowed_roles=['superadmin','Admin'])
def staff_password_reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password Reset Successfully')
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form
    }
    return render(request, 'staff/password_reset.html', context)

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'staffname':
        data = staff.objects.filter(
            first_name__istartswith=Searched,
            staff_school=sdata
        )

    else:
        data = staff.objects.filter(
            mobile__istartswith=Searched,
            staff_school=sdata
        )

    return render(request, 'staff/stafflist.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def homework_search(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    Searchby = request.POST['searchby']
    Searched = request.POST['searched'].strip()

    data = homework.objects.none()  # default empty

    # --- Title Search (Case insensitive) ---
    if Searchby == 'title':
        data = temp_homework.objects.filter(
            title__icontains=Searched,
            school_homework=sdata
        )

    # --- Class Search ---
    elif Searchby == 'hclass':
        try:
            homeclass = sclass.objects.get(
                name__iexact=Searched,   # make class matching case-insensitive
                acad_year=yr
            )
            data = temp_homework.objects.filter(hclass=homeclass, school_homework=sdata)
        except sclass.DoesNotExist:
            data = temp_homework.objects.none()

    # --- Subject Search ---
    elif Searchby == 'subj':
        try:
            homesubj = subjects.objects.get(
                subject_name__iexact=Searched,   # case-insensitive
                subject_year=year
            )
            data = temp_homework.objects.filter(subj=homesubj, school_homework=sdata)
        except subjects.DoesNotExist:
            data = temp_homework.objects.none()

    # --- Homework Date Search ---
    elif Searchby == 'homework_date':
        data = temp_homework.objects.filter(
            homework_date=Searched,
            school_homework=sdata
        )

    # --- Submission Date Search ---
    elif Searchby == 'submission_date':
        data = temp_homework.objects.filter(
            submission_date=Searched,
            school_homework=sdata
        )

    return render(
        request,
        'staff/homework.html',
        {'data': data, 'skool': sdata, 'year': year}
    )


@allowed_users(allowed_roles=['superadmin','Admin'])
def staff_import_csv(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('staff_import_csv')  # Redirect to the import page

        # Read the CSV file
        csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
        next(csv_data)  # Skip the header row

        try:
            for row in csv_data:
                # Ensure that the row has the correct number of columns
                if len(row) < 12:
                    messages.error(request, 'CSV file format is incorrect.')
                    return redirect('import_csv')

                # Create a new staff object and set its attributes from CSV data
                stf = staff()
                stf.first_name = row[0]
                stf.last_name = row[1]
                stf.gender = row[2]
                stf.dob = row[3]
                stf.father_spouse_name=row[4]
                stf.address = row[5]
                stf.mobile = row[6]
                stf.email = row[7]
                stf.join = row[8]
                stf.role = row[9]
                stf.salary = row[10]
                stf.desg = row[11]
                stf.qualification = row[12]
                stf.permission_group = row[13]
                stf.status = 'Active'
                stf.staff_school= sdata


                # Ensure unique email for User model
                email = row[7]
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email {email} already exists.')
                    return redirect('staff_import_csv')

                # Create a new user for the staff
                ruser = User.objects.create_user(username=email, email=email, password='Welcome@123')
                group = Group.objects.get(name='Teacher')
                ruser.groups.add(group)
                stf.staff_user=ruser
                # Save the staff object
                stf.save()

            messages.success(request, 'Staff imported successfully.')
            return redirect('stafflist')
        except Exception as e:
            err = f'{e}'
            messages.error(request, f'Staff import failed: {err}')
            return HttpResponse(err)

    return render(request, 'staff/import_csv.html', context={'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin','Admin'])
def download_staff_template(request):
    # Define the CSV headers
    headers = ['First Name', 'Last Name', 'Gender', 'Date of Birth','Father/Spouse Name', 'Address', 'Mobile', 'Email', 'Join Date', 'Role', 'Salary', 'Designation', 'Qualification','Permission Group']

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staff_template.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the headers to the CSV file
    writer.writerow(headers)

    return response

    
def homework_manual(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    today = timezone.localdate()  # gets current local date

    # filter today's homework for this school
    cpy = temp_homework.objects.filter(
        school_homework=sdata,
        homework_date=today
    )

    # prepare objects for bulk create
    homework_list = [
        homework(
            title=data.title,
            hclass=data.hclass,
            secs=data.secs,
            subj=data.subj,
            homework_date=data.homework_date,
            description=data.description,
            submission_date=data.submission_date,
            created_by=data.created_by,
            acad_yr=data.acad_yr,
            school_homework=data.school_homework,
            attachment=data.attachment
        )
        for data in cpy
    ]

    # insert all at once
    homework.objects.bulk_create(homework_list)

    return HttpResponse(f"Copied {len(homework_list)} homework(s) for {today}")
    
    
def homeworkreal_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.filter(school_homework=sdata).order_by('-id')
    return render(request,'staff/homework.html',context={'data':data,'skool':sdata,'year':year})


