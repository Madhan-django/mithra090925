from django.shortcuts import render,redirect
from .models import visitors
from .forms import add_visitorform
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from authenticate.decorators import allowed_users

from django.contrib import messages

# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def visitors_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = visitors.objects.filter(visitors_school=sch_id).order_by('check_in_time')
    return render(request, 'visitors/visitors.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def add_visitor(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'visitors_school' : sdata
    }
    if request.method == 'POST':
        form = add_visitorform(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Visitor added Successfully')
            return redirect('visitors_list')

    form = add_visitorform(initial=initial_data)
    return render(request,'visitors/add_visitors.html',context={'form':form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def update_visitor(request,visitor_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = visitors.objects.get(pk=visitor_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    form = add_visitorform(request.POST or None, instance=data)
    if form.is_valid():
        form.save()
        messages.success(request,'Visitor Updated Successfully')
        return redirect('visitors_list')
    return render(request,'visitors/update_visitors.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def delete_visitor(request,visitor_id):
   data = visitors.objects.get(pk=visitor_id)
   data.delete()
   messages.success(request,'Visitor Deleted Successfully')
   return redirect('visitors_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def view_visitor(request,visit_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = visitors.objects.get(pk=visit_id)
    return render(request, 'visitors/view_visitors.html', context={'data': data, 'skool': sdata, 'year': year})
