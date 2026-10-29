from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from institutions.models import school
from staff.forms import add_staff_form
from django.contrib import messages
from authenticate.decorators import allowed_users
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from .models import academicyr,currentacademicyr,sclass,section,subjects,receipt_template,homework_time,birthday_wish_config,AppUpdate,StaffAnnouncement
from .forms import add_Acad_Form,set_current_yr,add_class,add_section,add_subjects,receipt_template_form,add_homeworktime_form,birthday_wish_config_form,AppUpdateForm,StaffAnnouncementForm
from fees.models import SchoolPayUConfig
from django.utils import timezone
from datetime import datetime, timedelta
from django_q.models import Schedule
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO

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


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def birthday_wish_config_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    try:
        config = birthday_wish_config.objects.get(school=sdata)
    except birthday_wish_config.DoesNotExist:
        config = None
    return render(request, 'setup/birthday_wish_config.html', {
        'skool': sdata, 'year': year, 'config': config
    })


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def add_birthday_wish_config(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    try:
        existing = birthday_wish_config.objects.get(school=sdata)
    except birthday_wish_config.DoesNotExist:
        existing = None

    if request.method == 'POST':
        form = birthday_wish_config_form(request.POST, instance=existing)
        if form.is_valid():
            cfg = form.save()

            today = timezone.now().date()
            run_time = datetime.combine(today, cfg.time)
            run_time = timezone.make_aware(run_time, timezone.get_current_timezone())
            if run_time < timezone.now():
                run_time += timedelta(days=1)

            Schedule.objects.filter(
                func='pushnotify.tasks.send_birthday_wishes',
                name=f"Send Birthday Wishes Daily [{sdata.id}]"
            ).delete()

            if cfg.is_active:
                Schedule.objects.create(
                    func='pushnotify.tasks.send_birthday_wishes',
                    schedule_type=Schedule.DAILY,
                    next_run=run_time,
                    args=[sdata.id],
                    name=f"Send Birthday Wishes Daily [{sdata.id}]"
                )

            messages.success(request, "Birthday Wish Configuration Saved Successfully")
            return redirect('birthday_wish_config')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = birthday_wish_config_form(instance=existing, initial={'school': sdata})

    return render(request, 'setup/add_birthday_wish_config.html', {
        'skool': sdata, 'year': year, 'form': form
    })


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

@allowed_users(allowed_roles=['superadmin'])
def app_update_list(request):
    updates = AppUpdate.objects.order_by('-date')
    return render(request, 'setup/app_update_list.html', {'updates': updates})


@allowed_users(allowed_roles=['superadmin'])
def app_update_add(request):
    if request.method == 'POST':
        form = AppUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature update added successfully.')
            return redirect('app_update_list')
    else:
        form = AppUpdateForm()
    return render(request, 'setup/app_update_form.html', {'form': form, 'edit': False})


@allowed_users(allowed_roles=['superadmin'])
def app_update_edit(request, pk):
    update = AppUpdate.objects.get(pk=pk)
    if request.method == 'POST':
        form = AppUpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature update saved.')
            return redirect('app_update_list')
    else:
        form = AppUpdateForm(instance=update)
    return render(request, 'setup/app_update_form.html', {'form': form, 'edit': True, 'update': update})


@allowed_users(allowed_roles=['superadmin'])
def app_update_delete(request, pk):
    AppUpdate.objects.filter(pk=pk).delete()
    messages.success(request, 'Feature update deleted.')
    return redirect('app_update_list')


# ─── STAFF ANNOUNCEMENTS ─────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def announcement_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    items = StaffAnnouncement.objects.filter(school=sdata)
    return render(request, 'setup/announcement_list.html', {'items': items, 'skool': sdata})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def announcement_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    if request.method == 'POST':
        form = StaffAnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.school = sdata
            ann.posted_by = request.user
            ann.save()
            messages.success(request, 'Announcement posted successfully.')
            return redirect('announcement_list')
    else:
        form = StaffAnnouncementForm()
    return render(request, 'setup/announcement_form.html', {'form': form, 'edit': False, 'skool': sdata})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def announcement_edit(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    ann = StaffAnnouncement.objects.get(pk=pk, school=sdata)
    if request.method == 'POST':
        form = StaffAnnouncementForm(request.POST, instance=ann)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated.')
            return redirect('announcement_list')
    else:
        form = StaffAnnouncementForm(instance=ann)
    return render(request, 'setup/announcement_form.html', {'form': form, 'edit': True, 'ann': ann, 'skool': sdata})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def announcement_delete(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    StaffAnnouncement.objects.filter(pk=pk, school=sdata).delete()
    messages.success(request, 'Announcement deleted.')
    return redirect('announcement_list')


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

    return render(request, 'setup/payu_config.html', {
        'config': config,
        'skool':  sdata,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def download_subjects(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata, acad_year=yr)
    data = subjects.objects.filter(subject_school=sdata, subject_year=year).select_related('subject_class')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Subjects'

    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(fill_type='solid', fgColor='1F3864')
    center = Alignment(horizontal='center')

    headers = ['Subject Name', 'Subject Code', 'Class']
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 20

    for row_num, sub in enumerate(data, 2):
        ws.cell(row=row_num, column=1, value=sub.subject_name)
        ws.cell(row=row_num, column=2, value=sub.subject_code)
        ws.cell(row=row_num, column=3, value=sub.subject_class.name)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="subjects_{year.acad_year}.xlsx"'
    return response


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def download_subjects_sample(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Subjects'

    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(fill_type='solid', fgColor='1F3864')
    center = Alignment(horizontal='center')

    headers = ['Subject Name', 'Subject Code', 'Class']
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 20

    sample_rows = [
        ('Mathematics', 'MATH01', '1'),
        ('Science', 'SCI01', '1'),
        ('English', 'ENG01', '2'),
        ('Tamil', 'TAM01', '2'),
        ('Social Science', 'SOC01', '3'),
    ]
    for row_num, (name, code, cls) in enumerate(sample_rows, 2):
        ws.cell(row=row_num, column=1, value=name)
        ws.cell(row=row_num, column=2, value=code)
        ws.cell(row=row_num, column=3, value=cls)

    # Instructions sheet
    ws2 = wb.create_sheet(title='Instructions')
    ws2['A1'] = 'Instructions for uploading subjects:'
    ws2['A1'].font = Font(bold=True)
    notes = [
        'Column A (Subject Name): Full name of the subject, e.g. Mathematics',
        'Column B (Subject Code): Short code, e.g. MATH01',
        'Column C (Class): Must exactly match a class name already configured in the system',
        'Do not change the header row.',
        'Delete sample rows and enter your own data.',
    ]
    for i, note in enumerate(notes, 2):
        ws2['A' + str(i)] = note
    ws2.column_dimensions['A'].width = 70

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="subjects_sample.xlsx"'
    return response


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def upload_subjects(request):
    if request.method != 'POST':
        return redirect('listsubjects')

    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(school_name=sdata, acad_year=yr)

    xlsx_file = request.FILES.get('subjects_file')
    if not xlsx_file:
        messages.error(request, 'Please select a file to upload.')
        return redirect('listsubjects')

    if not xlsx_file.name.endswith('.xlsx'):
        messages.error(request, 'Only .xlsx files are supported.')
        return redirect('listsubjects')

    try:
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
    except Exception:
        messages.error(request, 'Invalid Excel file.')
        return redirect('listsubjects')

    classes = {c.name.strip().lower(): c for c in sclass.objects.filter(school_name=sdata, acad_year=yr)}

    created = 0
    skipped = 0
    errors = []

    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
        if not any(row):
            continue

        subject_name = str(row[0]).strip() if row[0] else ''
        subject_code = str(row[1]).strip() if row[1] else ''
        class_name   = str(row[2]).strip() if row[2] else ''

        if not subject_name or not class_name:
            errors.append(f'Row {row_num}: Subject Name and Class are required.')
            skipped += 1
            continue

        cls_obj = classes.get(class_name.lower())
        if not cls_obj:
            errors.append(f'Row {row_num}: Class "{class_name}" not found.')
            skipped += 1
            continue

        exists = subjects.objects.filter(
            subject_name=subject_name,
            subject_class=cls_obj,
            subject_year=year,
            subject_school=sdata
        ).exists()

        if exists:
            skipped += 1
            continue

        subjects.objects.create(
            subject_name=subject_name,
            subject_code=subject_code,
            subject_class=cls_obj,
            subject_year=year,
            subject_school=sdata
        )
        created += 1

    if errors:
        for e in errors[:5]:
            messages.warning(request, e)

    if created:
        messages.success(request, f'{created} subject(s) imported successfully.')
    if skipped:
        messages.info(request, f'{skipped} row(s) skipped (duplicates or errors).')
    return redirect('listsubjects')