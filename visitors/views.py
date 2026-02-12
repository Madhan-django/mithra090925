from django.shortcuts import render,redirect
from .models import visitors
from .forms import add_visitorform
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from authenticate.decorators import allowed_users
import base64
from django.core.files.base import ContentFile

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

    if request.method == 'POST':
        form = add_visitorform(request.POST)

        if form.is_valid():
            visitor = form.save(commit=False)

            # Handle webcam Base64 image
            img_data = request.POST.get("webcam_image")

            if img_data:
                format, imgstr = img_data.split(';base64,')
                ext = format.split('/')[-1]
                visitor.photo = ContentFile(base64.b64decode(imgstr), name="visitor."+ext)

            visitor.save()

            messages.success(request, "Visitor added Successfully")
            return redirect('visitors_list')

    initial_data = { 'visitors_school': sdata }
    form = add_visitorform(initial=initial_data)

    return render(request, 'visitors/add_visitors.html', {
        'form': form, 'skool': sdata, 'year': year
    })

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def update_visitor(request,visitor_id):

    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = visitors.objects.get(pk=visitor_id)

    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    if request.method == "POST":
        form = add_visitorform(request.POST, request.FILES, instance=data)

        if form.is_valid():
            visitor = form.save(commit=False)

            # HANDLE webcam Base64 image
            img_data = request.POST.get("webcam_image")
            if img_data:
                format, imgstr = img_data.split(';base64,')
                ext = format.split('/')[-1]
                visitor.photo = ContentFile(base64.b64decode(imgstr), name="visitor."+ext)

            visitor.save()

            messages.success(request, 'Visitor Updated Successfully')
            return redirect('visitors_list')

    else:
        form = add_visitorform(instance=data)

    return render(request,'visitors/update_visitors.html', {
        'form': form,
        'skool': sdata,
        'year': year,
        'data': data     # Send existing record to template for photo preview
    })


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

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def visitors_search(request):
    sch_id = request.session.get('sch_id')
    if sch_id is None:
        # Handle the case where 'sch_id' is not in the session, e.g., by raising a 404 error or redirecting
        raise Http404("School ID not found in session")

    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = visitors.objects.none()

    if request.method == 'POST':
        Searchby = request.POST.get('searchby', '')
        Searched = request.POST.get('searched', '')

        if Searchby == 'compname':
            data = visitors.objects.filter(company__istartswith=Searched, visitors_school=sdata)
        else:
            data = visitors.objects.filter(name__istartswith=Searched, visitors_school=sdata)

    return render(request, 'visitors/visitors.html',
                  context={'data': data, 'skool': sdata, 'year': year})
