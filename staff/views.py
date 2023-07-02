from django.shortcuts import render,redirect,HttpResponse
from .models import staff,staff_attendance,staff_attendancegen,homework
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,subjects
from .forms import add_staff_form,add_staff_attendance_gen,add_homework_form
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User,Group
from authenticate.decorators import allowed_users
from django.contrib.auth.forms import PasswordChangeForm
from .utils import render_to_pdf
import csv



# Create your views here.

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
    initial_data={
        'staff_school':sdata,
    }
    if request.method == 'POST':
        name_str = request.POST['first_name']
        name_str2 = request.POST['last_name']
        date_str1 = request.POST['dob']
        grp = request.POST['permission_group']
        eml = request.POST['email']
        name_str = name_str[0:3]
        name_str2 = name_str2[0:3]
        dtyr = date_str1[0:4]
        dtmon = date_str1[5:7]
        dt = date_str1[8:10]

        usernm = name_str + name_str2 + dt +dtmon + dtyr
        ruser = User.objects.create_user(username=usernm,
                                        email=eml,
                                        password='Welcome@123')

        group = Group.objects.get(name='Teacher')
        ruser.groups.add(group)
        form = add_staff_form(request.POST)
        if form.is_valid():
            chgusernm= form.save(commit=False)
            chgusernm.staff_user = ruser
            form.save()
            messages.success(request,'Staff has been added successfully')
            return redirect('stafflist')

    form = add_staff_form(initial=initial_data)
    context={'form':form,'skool':sdata}
    return render(request,'staff/add_staff.html',context)

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def staff_update(request, staff_id):
    data = staff.objects.get(pk=staff_id)
    form = add_staff_form(instance=data)
    if request.method=='POST':
        form = add_staff_form(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,' Staff Record Updated Successfully')
            return redirect('stafflist')
    context ={'form':form}
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
                messages.info('Attendance Not Available')
                return redirect('staff_viewattendance')
    return render(request,'staff/viewattendance.html',context={'form':form,'skool':sdata})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_homework(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    hclass = sclass.objects.filter(school_name=sdata)
    user = request.user.id
    usr = User.objects.get(id=user)
    initial_data = {
        'acad_yr':yr,
        'school_homework':sdata,

    }
    if request.method == 'POST':
        form = add_homework_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Homework Added Successfully')
            return redirect('homework')
        else:
            messages.info(request,'Invalid Data')
            return redirect('homework')  # Redirect to the homework list view
    else:
        form = add_homework_form(initial=initial_data)

    return render(request, 'staff/add_homework.html',{'form':form,'hclass':hclass,'skool':sdata,'usr':usr})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def homework_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.filter(school_homework=sdata)
    return render(request,'staff/homework.html',context={'data':data,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_homework(request,homework_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.get(pk=homework_id)
    form = add_homework_form(instance=data)
    if request.method == 'POST':
        form = add_homework_form(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homework Updated Successfully')
            return redirect('homework')
    context = {'form': form,'skool':sdata,'year':year}
    return render(request, 'staff/update_homework.html', context)


@allowed_users(allowed_roles=['superadmin','Admin'])
def delete_homework(request,homework_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.get(pk=homework_id)
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
        data = staff.objects.filter(first_name__startswith=Searched)
    else:
        data = staff.objects.filter(mobile__startswith=Searched)
    return render(request, 'staff/stafflist.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def homework_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'title':
        data = homework.objects.filter(title__startswith=Searched)
    elif Searchby == 'hclass':
        homeclass = sclass.objects.get(name=Searched,acad_year=yr)
        data = homework.objects.filter(hclass=homeclass)
    elif Searchby == 'subj':
        homesubj = subjects.objects.get(subject_name=Searched,subject_year=year)
        data = homework.objects.filter(subj=homesubj)
    elif Searchby == 'homework_date':
        data = homework.objects.filter(homework_date=Searched)
    else:
        data = homework.objects.filter(submission_date=Searched)
    return render(request, 'staff/homework.html', context={'data': data, 'skool': sdata, 'year': year})
