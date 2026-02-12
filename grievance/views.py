from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from authenticate.decorators import allowed_users
from institutions.models import school
from setup.models import currentacademicyr,academicyr,sclass,section
from admission.models import students
from .models import Grievance
from .forms import GrievanceForm, GrievanceupdateForm

# Create your views here.

#  LIST VIEW
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def grievance_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    grievances = Grievance.objects.filter(gschool=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    return render(request,'grievance/grievances.html',context={'skool':sdata,'year':year,'cls':cls,'grievances':grievances})



#  CREATE VIEW
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def grievance_create(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    initial_data= {
        'gschool':sdata,
        'ac_year':year
    }
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grievance successfully submitted.")
            return redirect('grievance_list')
    else:
        form = GrievanceForm(initial=initial_data)
        form.fields['gclass'].queryset=cls
        form.fields['gsec'].queryset = section.objects.none()

    return render(request, 'grievance/grievance_form.html', {
        'form': form,
        'title': "New Grievance",
        'skool':sdata,
        'year':year
    })



#  UPDATE VIEW
@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def grievance_update(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    grievance = get_object_or_404(Grievance, pk=pk)

    if request.method == 'POST':
        form =  GrievanceupdateForm(request.POST, instance=grievance)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.no_action_taken = False
            temp.save()
            messages.success(request, "Grievance updated successfully.")
            return redirect('grievance_list')
        else:
            return HttpResponse(form.errors)
    else:
        form = GrievanceupdateForm(instance=grievance)

    return render(request, 'grievance/grievanceupdate_form.html', {
        'form': form,
        'title': "Update Grievance",
        'skool':sdata,
        'year':year
    })



#  DELETE VIEW
@allowed_users(allowed_roles=['superadmin','Admin'])
def grievance_delete(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk)
    grievance.delete()
    messages.success(request, "Grievance deleted.")
    return redirect('grievance_list')






def ajax_load_students(request):
    class_id = request.GET.get('class_id')
    sec_id = request.GET.get('sec_id')

    students_list = students.objects.filter(
        class_name=class_id,
         secs=sec_id
    ).order_by('first_name')
    return render(request, 'grievance/student_dropdown_list.html', {
        'students': students_list
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts', 'Teacher'])
def grievance_search(request):
    sch_id = request.session.get('sch_id')
    if sch_id is None:
        raise Http404("School ID not found in session")

    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = Grievance.objects.none()

    # Handle both GET and POST
    if request.method == 'POST':
        Searchby = request.POST.get('searchby', '')
        Searched = request.POST.get('searched', '')
        class_id = request.POST.get('class_name')
        section_id = request.POST.get('section_name')
    else:
        Searchby = request.GET.get('searchby', '')
        Searched = request.GET.get('searched', '')
        class_id = request.GET.get('class_name')
        section_id = request.GET.get('section_name')

    # === Main search logic ===
    if Searchby:
        if Searchby == 'studname' and Searched:
            data = Grievance.objects.filter(stud_name__first_name__istartswith=Searched, gschool=sdata)
        elif Searchby == 'cdate' and Searched:
            data = Grievance.objects.filter(complaint_date=Searched, gschool=sdata)
        elif Searchby == 'mobno' and Searched:
            data = Grievance.objects.filter(mobile__startswith=Searched, gschool=sdata)
        elif Searchby == 'comptype' and Searched:
            data = Grievance.objects.filter(area_of_complaint=Searched, gschool=sdata)
        elif Searchby == 'compstatus' and Searched:
            data = Grievance.objects.filter(complaint_status__icontains=Searched, gschool=sdata)
        else:
            data = Grievance.objects.none()

    # === CLASS/SECTION FILTER ALWAYS APPLIED IF SELECTED ===
    if class_id or section_id:
        filters = {'gschool': sdata}

        if class_id and class_id != "":
            filters['gclass__id'] = class_id

        if section_id and section_id != "":
            filters['gsec__id'] = section_id

        # If there is already search data, filter within it
        if data.exists():
            data = data.filter(**filters)
        else:
            data = Grievance.objects.filter(**filters)

    cnt = data.count()

    return render(request, 'grievance/grievances.html', {
        'grievances': data,
        'skool': sdata,
        'year': year,
        'cnt': cnt,
        'cls': sclass.objects.filter(school_name=sdata, acad_year=year),
    })

