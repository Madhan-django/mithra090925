from django.shortcuts import render,redirect,HttpResponse,reverse
from django.contrib import messages
from django.forms import modelformset_factory
from .models import exams,exam_subjectmap,admit_card,temp_insert,exam_result
from .forms import add_exam_form,add_exam_subjectmap_form,temp_insert_form
from institutions.models import school
from authenticate.decorators import allowed_users
from setup.models import academicyr,currentacademicyr,subjects,sclass
from admission.models import students
from .utils import render_to_pdf


# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def exam_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exams.objects.filter(exam_school=sch_id,exam_year=year)
    return render(request,'exams/exams.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_exams(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=yr)
    initial_data={
         'exam_year':year,
         'exam_school':sdata
    }
    if request.method == 'POST':
        form= add_exam_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Exam Added Successfully')
            return redirect('examlist')

    form = add_exam_form(initial=initial_data)
    return render(request,'exams/addexam.html',context={'form':form,'cls':cls,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_exams(request,exam_id):
    exam_data = exams.objects.get(pk=exam_id)
    if request.method=='POST':
        form = add_exam_form(request.POST or None,instance=exam_data)
        if form.is_valid():
            form.save()
            messages.success(request,'Exam Updated Successfully')
            return redirect('examlist')
    form = add_exam_form(instance=exam_data)
    return render(request,'exams/updateexam.html',context={'form':form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def delete_exams(request,exam_id):
    exam_data= exams.objects.get(pk=exam_id)
    exam_data.delete()
    messages.info(request,'Exam Deleted Successfully')
    return redirect('examlist')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def exams_subject(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exam_subjectmap.objects.filter(exname__exam_school=sdata,exname__exam_year=year)
    return render(request,'exams/exams_subject.html',context={'data':data,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_exam_subject(request,exam_id):
    exam_data = exams.objects.get(pk=exam_id)
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = subjects.objects.filter(subject_class=exam_data.exam_class)
    initial_data = {
        'exname': exam_data,

    }
    if request.method == 'POST':
        form = add_exam_subjectmap_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam Subject Added Successfully')
            return redirect('exam_list')
        else:
            print('invalid form')
    form = add_exam_subjectmap_form(initial=initial_data)
    return render(request,'exams/add_exam_subject.html',context={'form':form,'cls':cls,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_exam_subject(request,exam_subject_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exam_subjectmap.objects.get(pk=exam_subject_id)
    form = add_exam_subjectmap_form(instance=data)
    if request.method=='POST':
        form = add_exam_subjectmap_form(request.POST or None,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Exam Subject updated Successfully')
            return redirect('exams_subject')
    return render(request,'exams/update_exam_subject.html',context={'form':form,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin'])
def delete_exam_subject(request,exam_subject_id):
    data = exam_subjectmap.objects.get(pk=exam_subject_id)
    data.delete()
    messages.info(request, 'Exam Subject Deleted Successfully')
    return redirect('exams_subject')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def admit_card_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exams.objects.filter(exam_school=sdata,exam_year=year)
    return render(request,'exams/admit_card.html',{'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def generate_admit_card(request,exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    exam_data = exams.objects.get(pk=exam_id)
    ex_sub = exam_subjectmap.objects.filter(exname=exam_data)
    print(ex_sub)
    if request.method == 'POST':
        form = temp_insert_form(request.POST)
        if form.is_valid():
            prefx=form.cleaned_data['exam_prefix']
            start_no = form.cleaned_data['exam_start_no']
            stud = students.objects.filter(school_student=sdata,ac_year=year,class_name=exam_data.exam_class,student_status='Active')
            for exam_stud in stud:
                start_str= str(start_no)
                exam_numb = prefx+start_str
                admit_card.objects.create(examno=exam_numb,exam_stu=exam_stud,exam_label=exam_data)
                start_no = int(start_no)
                admt = admit_card.objects.get(exam_stu=exam_stud,exam_label=exam_data)
                for subj in ex_sub:
                    exam_result.objects.create(exam_sub=subj,adm_card=admt)

                start_no = start_no + 1
    admt = admit_card.objects.filter(exam_label=exam_data)
    return render(request,'exams/generate_admitcard.html',context={'data':admt,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_formset(request,exam_det_id,exam_label_id):
    test = admit_card.objects.get(pk=exam_det_id)
    MyModelFormSet = modelformset_factory(exam_result, fields=('obtained_marks', 'exam_sub', 'adm_card', 'remark'),extra=0)
    formset = MyModelFormSet(request.POST or None, queryset=exam_result.objects.filter(adm_card__examno=test,adm_card__exam_label=test.exam_label))
    data = exam_result.objects.filter(adm_card__examno=test)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            messages.success(request,'Mark update successfully')
            dynamic_url = reverse('generate_admit_card', args=[exam_label_id])
            return redirect(dynamic_url)

        else:
            messages.success(request, 'invalid form')
    return render(request, 'exams/update_formset.html', {'formset': formset,'data':test})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def exam_result_view(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = admit_card.objects.all()
    clsdata = sclass.objects.filter(acad_year=yr, school_name=sdata)
    return render(request,'exams/exam_result.html',context={'data':data,'clsdata':clsdata,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def exam_result_print(request,admit_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exam_result.objects.filter(adm_card=admit_id)
    adm_data = admit_card.objects.get(pk=admit_id)
    tot=0
    for total in data:
        tot = tot + total.obtained_marks
    edata={
        'data':data,
        'skool':sdata,
        'adm_data':adm_data,
        'tot':tot
    }
    pdf = render_to_pdf('exams/print_exam_result.html',edata)
    return HttpResponse(pdf, content_type='application/pdf')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def bulk_print_result(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    if request.method == 'POST':
        selcls = request.POST.get('selectcls')
        cls = sclass.objects.get(pk=selcls)
        stud = students.objects.filter(class_name=cls)
        exm = exams.objects.filter(exam_class=cls)
        subj = subjects.objects.filter(subject_class=cls)
        print('sub:-', subj)
        data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls)

        edata = {
            'data': data,
            'stud': stud,
            'exm': exm,
            'subj': subj,
            'skool': sdata
        }

        pdf = render_to_pdf('exams/bulk_print_result.html', edata)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="bulk_result.pdf"'
            return response
        else:
            # Handle the case when PDF generation fails
            return HttpResponse("Failed to generate PDF.", status=500)
    else:
        # Handle GET request or other cases
        return HttpResponse("Invalid request method.", status=400)

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def delete_admit_card(request,exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    exam_data = exams.objects.get(pk=exam_id)
    admt = admit_card.objects.filter(exam_label=exam_data)
    admt.delete()
    return redirect('admit_card_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def print_adm_card(request,exam_no):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    adm_data = admit_card.objects.filter(examno=exam_no)
    adm_data2 = admit_card.objects.filter(examno=exam_no)[:1].get()

    examsub = exam_subjectmap.objects.filter(exname__exam_class=adm_data2.exam_stu.class_name)

    adm={
        'data':adm_data,
        'skool':sdata,
        'year':year,
        'examsub':examsub,
    }
    pdf = render_to_pdf('exams/print_adm_card.html',adm )
    return HttpResponse(pdf, content_type='application/pdf')











