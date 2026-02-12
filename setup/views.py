from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from institutions.models import school
from staff.forms import add_staff_form
from django.contrib import messages
from authenticate.decorators import allowed_users
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from .models import academicyr,currentacademicyr,sclass,section,subjects,receipt_template,homework_time
from .forms import add_Acad_Form,set_current_yr,add_class,add_section,add_subjects,receipt_template_form,add_homeworktime_form
from django.utils import timezone
from datetime import datetime, timedelta
from django_q.models import Schedule

# Create your views here.
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def academicyear(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = academicyr.objects.filter(school_name=sch_id)
    return render(request,'setup/academic-year.html',context={'data':data,'sch':sdata,'skool':sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def add_acad_yr(request):
    sch_id = request.session['sch_id']
    sch = school.objects.get(id=sch_id)
    initial_data = {
        'school_name':sch_id
    }
    if request.method=='POST':
        form = add_Acad_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Session Added Successfully')
            return redirect('academicyr')
    form = add_Acad_Form(initial=initial_data)
    return render(request,'setup/add_acad_yr.html',context={'form':form,'sch':sch})

@allowed_users(allowed_roles=['superadmin','Admin'])
def del_acad_yr(request,acadyr_id):
    data = academicyr.objects.get(pk=acadyr_id)
    data.delete()
    messages.success(request,'Academic Year deleted Successfully')
    return redirect('academicyr')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def current_acad_yr(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    ydata = academicyr.objects.filter(school_name=sch_id)

    try:
        adata = currentacademicyr.objects.get(school_name=sch_id)
        form= None;
    except currentacademicyr.DoesNotExist:
        # If current academic year is not set, create a form to set it
        initial_data = {
            'school_name': sdata
        }
        form = set_current_yr(initial=initial_data)
        adata= None;

    if request.method == 'POST':
        form = set_current_yr(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Current Academic Year has been Set Successfully')
            return redirect('set_current_yr')

    return render(request, 'setup/set_current.html',
                  context={'form':form,'adata': adata, 'skool': sdata, 'ydata': ydata, 'sdata': sdata})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def update_acad_yr(request,acadyr_id):
    sch_id = request.session['sch_id']
    skool = school.objects.get(pk=sch_id)
    data = currentacademicyr.objects.get(pk=acadyr_id)
    syear = academicyr.objects.filter(school_name=skool)

    if request.method =='POST':
        form = set_current_yr(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'current year changed')

    form = set_current_yr(instance=data)

    return render(request,'setup/update_current.html',context={'form':form,'syear':syear,'sch':skool,'skool':skool})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def listsclass(request):
    sch_id = request.session['sch_id']
    skool = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    classdet = sclass.objects.filter(school_name=sch_id,acad_year=year)
    return render(request,'setup/sclass.html',context={'data':classdet,'skool':skool,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def delcls(request,cls_id):
    if request.method=='POST':
        cls = sclass.objects.get(pk=cls_id)
        cls.delete()
    return HttpResponseRedirect('listclass')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addclass(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year= currentacademicyr.objects.get(school_name=sdata)
    intial_data={
            'acad_year': year,
            'school_name':sdata
        }
    if request.method=='POST':
        form = add_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('listclass')
    form=add_class(initial=intial_data)
    return render(request,'setup/addclass.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updateclass(request,cls_id):
    data = sclass.objects.get(pk=cls_id)
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sdata)
    form = add_class(request.POST or None,instance=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Class Updated Successfully')
            return redirect('listclass')
    return render(request,'setup/updateclass.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def listsec(request):
    sch_id = request.session['sch_id']
    skool = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data= section.objects.filter(school_name=sch_id,acad_year=year)
    return render(request,'setup/ssec.html',context={'data':data,'skool':skool,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def delsec(request,sec_id):
    data = section.objects.get(pk=sec_id)

    data.delete()
    messages.info(request,'Section Deleted Successfully')
    return redirect('listsec')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updatesec(request,sec_id):
    data = section.objects.get(pk=sec_id)
    sch_id = request.session['sch_id']
    skool = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)

    form = add_section(request.POST or None,instance=data)
    if form.is_valid():
        form.save()
        return redirect('listsec')
    return render(request,'setup/updatesec.html',context={'form':form,'skool':skool,'year':year})

def load_section(request):
    profession_id = request.GET.get('profession')
    ssection = section.objects.filter(class_sec_name=profession_id).order_by('class_sec_name')
    print(ssection)
    return render(request, 'setup/professioncategory2_dropdown_list_options.html',context={'ssection': ssection})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addsec(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    cdata = sclass.objects.filter(school_name=sdata).values()
    year = currentacademicyr.objects.get(school_name=sch_id)
    initial_data={
        'acad_year':year,
        'school_name':sch_id
    }
    if request.method == 'POST':
        form=add_section(request.POST)
        if form.is_valid():
            messages.success(request, 'Section Added Successfully')
            form.save()
            return redirect('listsec')
    form = add_section(initial=initial_data)
    return render(request, 'setup/addsec.html', context={'form': form,'options':cdata,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def subjects_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr= currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata,acad_year=yr)
    cpyears = academicyr.objects.filter(school_name=sdata)
    data = subjects.objects.filter(subject_school=sdata,subject_year=year)
    return render(request,'setup/subjects.html',context={'skool':sdata,'year':year,'data':data,'cpyears':cpyears})

@allowed_users(allowed_roles=['superadmin','Admin'])
def delsubject(request, sublst_id):
    sub = subjects.objects.get(pk=sublst_id)
    sub.delete()
    messages.info(request,'Subject Deleted Successfully')
    return redirect('listsubjects')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def addsubject(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata, acad_year=yr)
    cls = sclass.objects.filter(school_name=sdata)
    intial_data = {

        'subject_school': sdata,
        'subject_year':year
    }
    if request.method == 'POST':
        form = add_subjects(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject Added Successfully')
            return HttpResponseRedirect('listsubjects')
    form = add_subjects(initial=intial_data)
    return render(request, 'setup/addsubjects.html', context={'form': form,'skool':sdata,'year':year,'cls':cls})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updatesubject(request, sublst_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata, acad_year=yr)
    data = subjects.objects.get(pk=sublst_id)
    if request.method == 'POST':
        form = add_subjects(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully')
            return redirect('listsubjects')
    form = add_subjects(instance=data)
    return render(request, 'setup/updatesubjects.html', context={'form': form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def edit_academic_yr(request, acadyr_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    # Fetch the academic year instance
    data = academicyr.objects.get(pk=acadyr_id)

    if request.method == "POST":
        form = add_Acad_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session Updated Successfully')
            return redirect('academicyr')

    form = add_Acad_Form(instance=data)

    return render(request, 'setup/update_academicyr.html', {'form': form,'skool':sdata})


@allowed_users(allowed_roles=['superadmin','Admin'])
def add_admin(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    ggrp = Group.objects.exclude(name='superadmin')
    initial_data = {
        'staff_school': sdata,
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

        usernm = name_str + dt + dtmon + dtyr
        ruser = User.objects.create_user(username=usernm,
                                         email=eml,
                                         password='Welcome@123')

        group = Group.objects.get(id=grp)
        ruser.groups.add(group)
        form = add_staff_form(request.POST)
        if form.is_valid():
            chgusernm = form.save(commit=False)
            chgusernm.staff_user = ruser
            form.save()
            messages.success(request, 'Staff has been added successfully')
            return redirect('stafflist')

    form = add_staff_form(initial=initial_data)
    context = {'form': form, 'skool': sdata,'ggrp':ggrp}
    return render(request, 'setup/add_staff.html', context)       




@allowed_users(allowed_roles=['superadmin','Admin'])
def reset_password(request,user_nm):
    new_password = 'Welcome@123'
    user = User.objects.get(username=user_nm)
    user.set_password(new_password)
    user.save()
    messages.success(request, 'Password Reset Successfully')
    groups = user.groups.all()
    if groups.filter(name='admin').exists():
        return redirect('/')

    elif groups.filter(name='Teacher').exists():
        return redirect('stafflist')

    else:
        return redirect('students_list')


def add_receipt_template(request):
    sch_id = request.session['sch_id']
    sch = school.objects.get(id=sch_id)
    initial_data = {
        'school_name':sch_id
    }
    if request.method=='POST':
        form = receipt_template_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Receipt Template Added Successfully')
            return redirect('home_dashboard')
        else:
            return HttpResponse(form.errors)
    form = receipt_template_form(initial=initial_data)
    return render(request,'setup/add_receipt_template.html',context={'form':form,'sch':sch})

def show_receipt_template(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(id=sch_id)
    data = receipt_template.objects.filter(school_name=sdata)
    return render(request, 'setup/show_receipt_template.html', context={'data': data, 'skool': sdata})

def del_receipt_template(request, sublst_id):
    sub = receipt_template.objects.get(id=sublst_id)
    sub.delete()
    messages.info(request,'Template  Deleted Successfully')
    return redirect('show_receipt_template')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def update_receipt_template(request, sublst_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    initial_data = {
        'school_name': sdata
    }
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata, acad_year=yr)
    data = receipt_template.objects.get(pk=sublst_id)
    if request.method == 'POST':
        form = receipt_template_form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully')
            return redirect('show_receipt_template')
    form = receipt_template_form(initial=initial_data)
    return render(request, 'setup/add_receipt_template.html', context={'form': form, 'skool': sdata})
    
    
@allowed_users(allowed_roles=['superadmin','Admin'])
def homeworktime(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework_time.objects.filter(homework_school=sdata)
    return render(request,'setup/homework_time.html',context={'skool':sdata,'year':year,'data':data})



@allowed_users(allowed_roles=['superadmin','Admin'])
def add_homeworktime(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    initial_data = {'homework_school': sdata}

    # Load existing record if available
    try:
        existing_time = homework_time.objects.get(homework_school=sdata)
    except homework_time.DoesNotExist:
        existing_time = None

    if request.method == 'POST':
        form = add_homeworktime_form(request.POST, instance=existing_time)
        if form.is_valid():
            tme = form.save()

            # Combine today's date with the selected time
            today = timezone.now().date()
            run_time = datetime.combine(today, tme.time)
            run_time = timezone.make_aware(run_time, timezone.get_current_timezone())

            # If the selected time has already passed today, schedule for tomorrow
            if run_time < timezone.now():
                run_time += timedelta(days=1)

            # Delete old schedules for this school (clean up)
            Schedule.objects.filter(
                func='staff.tasks.send_homework',
                name=f"Send Homework Daily [{sdata.id}]"
            ).delete()

            # Create new daily schedule
            Schedule.objects.create(
                func='staff.tasks.send_homework',
                schedule_type=Schedule.DAILY,
                next_run=run_time,
                args=[sdata.id],
                name=f"Send Homework Daily [{sdata.id}]"
            )

            messages.success(request, "Homework Time and Schedule Updated Successfully")
            return redirect('homeworktime')
        else:
            messages.error(request, "Invalid Time")
    else:
        form = add_homeworktime_form(instance=existing_time, initial=initial_data)

    return render(
        request,
        'setup/add_homeworktime.html',
        context={'skool': sdata, 'year': year, 'form': form}
    )


def test_delete(request):
    Schedule.objects.filter(args__contains='[[').delete()
    return HttpResponse("ok")


allowed_users(allowed_roles=['superadmin','Admin'])
def copysubjects(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    # get current academic year
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # get subjects of current year
    subj = subjects.objects.filter(subject_year=year, subject_school=sdata)

    if request.method == 'POST':
        copyyear_id = request.POST.get('cpyyear')   # 👈 read from POST
        if not copyyear_id:
            messages.error(request, "Please select a year to copy subjects.")
            return redirect('listsubjects')

        copyyear = academicyr.objects.get(id=copyyear_id)

        # copy subjects
        for sub in subj:
            subjects.objects.create(
                subject_name=sub.subject_name,
                subject_code=sub.subject_code,
                subject_year=copyyear,
                subject_class=sub.subject_class,
                subject_school=sub.subject_school
            )

        messages.success(request, f"Subjects copied to {copyyear.acad_year} successfully.")
    return redirect('listsubjects')  # 👈 redirect back to subject list

