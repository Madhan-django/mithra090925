from django.shortcuts import render,HttpResponse,redirect
from .models import noticeboard,events
from institutions.models import school
from setup.models import academicyr,currentacademicyr
from .forms import NoticeBoardForm,add_event_form
from django.contrib import messages
from authenticate.decorators import allowed_users





# Create your views here.
@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def academic_dashboard(request):
    return HttpResponse('Dashboard')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def academic_noticeboard(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = noticeboard.objects.filter(notice_school=sdata).order_by('-notice_date')
    return render(request,'academic/noticeboard.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_noticeboard(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'notice_school':sdata
    }
    if request.method == 'POST':
        form = NoticeBoardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Handle successful form submission (e.g., redirect or render a success message)
    else:
        form = NoticeBoardForm(initial=initial_data)
    return render(request, 'academic/add_noticeboard.html', {'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_noticeboard(request,notice_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = noticeboard.objects.get(pk=notice_id)
    if request.method == 'POST':
        form = NoticeBoardForm(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Notice Board Updated Successfully')
            return redirect('academic_noticeboard')
    else:
        form = NoticeBoardForm(instance=data)
    return render(request,'academic/update_noticeboard.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def delete_noticeboard(request,notice_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = noticeboard.objects.get(pk=notice_id)
    data.delete()
    messages.warning(request,'Notice deleted Successfully')
    return redirect('academic_noticeboard')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def academic_events(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.filter(event_school=sdata).order_by('-start_date')
    return render(request,'academic/events.html',context={'data':data,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_event(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data={
        'event_school':sdata
    }
    if request.method == 'POST':
        form = add_event_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Event added Successfully')
            return redirect('academic_events')
    else:
        form = add_event_form(initial=initial_data)

    return render(request, 'academic/add_event.html',context={'form': form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_event(request,event_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.get(pk=event_id)
    if request.method == 'POST':
        form = add_event_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event Updated Successfully')
            return redirect('academic_events')
    else:
        form = add_event_form(instance=data)
    return render(request, 'academic/update_event.html', context={'form': form, 'skool': sdata, 'year': year,'data':data})

@allowed_users(allowed_roles=['superadmin','Admin',])
def delete_event(request,event_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.get(pk=event_id)
    data.delete()
    messages.success(request,'Event Deleted Successfully')
    return redirect('academic_events')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def noticeboard_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'title':
        data = noticeboard.objects.filter(title__startswith=Searched,notice_school=sdata)
    else:
        data = noticeboard.objects.filter(notice_date=Searched,notice_school=sdata)
    return render(request, 'academic/noticeboard.html', context={'data': data, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def event_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'event_title':
        data = events.objects.filter(event_title__startswith=Searched,event_school=sdata)
    elif Searchby == 'start_date':
        data = events.objects.filter(start_date=Searched,event_school=sdata)
    else:
        data = events.objects.filter(event_location__startswith=Searched)
    return render(request, 'academic/events.html', context={'data': data, 'skool': sdata, 'year': year})
