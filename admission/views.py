import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from institutions.models import school
from setup.models import currentacademicyr,sclass,section,academicyr
from .models import enquiry
from .forms import add_enq_form,add_studentsForm
from authenticate.decorators import allowed_users
import datetime
from django.contrib import messages


# Create your views here.
@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def enquiry_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = enquiry.objects.filter(school_name=sch_id,acad_year=year)
    return render(request,'admission\enquiry_list.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_enquiry(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    intial_data = {
        'school_name':sdata,
        'acad_year':year
    }
    if request.method == 'POST':
        form= add_enq_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Enquiry Added Successfully')
        else:
            messages.info(request,'Form Invalid')
    form = add_enq_form(initial=intial_data)
    return render(request,'admission/add_enquiry.html',context={'form':form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin'])
def del_enquiry(request,enq_id):
    data = enquiry.objects.get(pk=enq_id)
    data.delete()
    messages.success(request,'Enquiry Deleted Successfully')
    return redirect('enquiry_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_enquiry(request,enq_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = enquiry.objects.get(pk=enq_id)
    form = add_enq_form(request.POST or None, instance=data)
    if form.is_valid():
        form.save()
        messages.success(request,'Enquiry Updated Successfully')
        return redirect('enquiry_list')

    return render(request,'admission/update_enquiry.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def followup_enquiry(request):
    tooday = datetime.date.today()
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = enquiry.objects.filter(enq_followup=tooday).exclude(enq_status='Closed')
    return render(request,'admission/followup_enquiry.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def search_enquiry(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    if request.method== 'POST':
        srch = request.POST['searched']
        srchby = request.POST['searchby']
        if srchby == 'enq_student':
            data = enquiry.objects.filter(enq_student__icontains=srch)
        elif srchby == 'enq_name':
            data = enquiry.objects.filter(enq_name__icontains=srch)
        else:
            data = enquiry.objects.filter(enq_date=srch)

        print('search-',srch,'searchby-',srchby)
        return render(request,'admission/search_enquiry.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def addstudents(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    cdata = sclass.objects.filter(school_name=sdata).values()
    year = currentacademicyr.objects.get(school_name=sch_id)
    yr = academicyr.objects.get(school_name=sch_id,acad_year=year)
    initial_data = {
        'ac_year':yr,
        'school_student':sdata,
    }
    if request.method == 'POST':
        form = add_studentsForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['usernm']
            eml = form.cleaned_data['email']
            if user is not None:
                print('user present')
                if User.objects.filter(username=user).exists():
                    messages.warning(request,'User already Exist')
                tmp = User.objects.create(username=user,email=eml, password='welcome@123')
                grp = Group.objects.get(name='student')
                tmp.groups.add(grp)

            form.save()
            messages.success(request, 'Student Admitted Successfully')
            return redirect('students_list')
    form = add_studentsForm(initial=initial_data)
    return render(request,'admission/Admit.html',context={'form':form,'cdata':cdata,'skool':sdata,'year':year})

def load_section(request):
    class_id = request.GET.get('Class_Id')
    ssection = section.objects.filter(class_sec_name=class_id).order_by('class_sec_name')
    return render(request, 'admission/selectsection.html',context={'ssection': ssection})


