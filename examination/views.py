from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.forms import modelformset_factory
from .models import exams,exam_subjectmap,admit_card,temp_insert,exam_result,exam_group
from .forms import add_exam_form,add_exam_subjectmap_form,temp_insert_form,exam_resultform,exam_groupform
from institutions.models import school
from authenticate.decorators import allowed_users
from setup.models import academicyr,currentacademicyr,subjects,sclass,section
from admission.models import students

from .utils import render_to_pdf
from django.db.models import Avg
from django.conf import settings
from django.http import JsonResponse
import openpyxl
from openpyxl.styles import Font
from io import BytesIO
import os
# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def exam_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exams.objects.filter(exam_school=sch_id,exam_year=year).order_by('-exam_start_date')
    return render(request,'exams/exams.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def add_exams(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=yr)
    exgrp = exam_group.objects.filter(exam_group_school=sdata)
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
    return render(request,'exams/addexam.html',context={'form':form,'cls':cls,'skool':sdata,'year':year,'exgrp':exgrp})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_exams(request,exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=yr)
    exgrp = exam_group.objects.filter(exam_group_school=sdata)
    exam_data = exams.objects.get(pk=exam_id)
    ex_cls = exam_data.exam_class
    ex_grp = exam_data.exm_grp
    if request.method=='POST':
        form = add_exam_form(request.POST or None,instance=exam_data)
        if form.is_valid():
            form.save()
            messages.success(request,'Exam Updated Successfully')
            return redirect('examlist')
    form = add_exam_form(instance=exam_data)
    return render(request,'exams/updateexam.html',context={'form':form,'cls':cls,'skool':sdata,'year':year,'exgrp':exgrp,'ex_cls':ex_cls,'ex_grp':ex_grp})

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts', 'Teacher'])
def clone_exams(request, exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=yr)
    exgrp = exam_group.objects.filter(exam_group_school=sdata)
    # Retrieve the existing exam_data
    existing_exam = exams.objects.get(pk=exam_id)
    ex_cls = existing_exam.exam_class

    if request.method == 'POST':
        # Clone the existing exam_data
        new_exam_data = existing_exam
        new_exam_data.pk = None  # Set to None to create a new instance

        # Create a form with the POST data and the cloned instance
        form = add_exam_form(request.POST, instance=new_exam_data)

        if form.is_valid():
            form.save()
            messages.success(request, 'Exam Updated Successfully')
            return redirect('examlist')
    else:
        # If the request method is not POST, create a form with the existing instance
        form = add_exam_form(instance=existing_exam)

    return render(request, 'exams/cloneexam.html', context={'form': form,'cls':cls,'exgrp':exgrp,'skool':sdata,'year':year,'ex_cls':ex_cls})




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
    cls = subjects.objects.filter(subject_class=exam_data.exam_class,subject_year=year)
    initial_data = {
        'exname': exam_data,

    }
    if request.method == 'POST':
        form = add_exam_subjectmap_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam Subject Added Successfully')
            
        else:
            print('invalid form')
    form = add_exam_subjectmap_form(initial=initial_data)
    return render(request,'exams/add_exam_subject.html',context={'form':form,'cls':cls,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_exam_subject(request, exam_subject_id):

    sch_id = request.session.get('sch_id')
    sdata = get_object_or_404(school, pk=sch_id)

    yr = get_object_or_404(currentacademicyr, school_name=sdata)
    year = get_object_or_404(academicyr, acad_year=yr, school_name=sdata)

    data = get_object_or_404(
        exam_subjectmap,
        pk=exam_subject_id,
        exname__exam_school=sdata   # 🔐 school-level safety
    )

    subj = subjects.objects.filter(
        subject_class=data.exname.exam_class,
        subject_year=year
    )

    exms = exams.objects.filter(exam_school=sdata)

    if request.method == 'POST':
        form = add_exam_subjectmap_form(request.POST, instance=data)
        form.fields['exname'].queryset = exms   # ✅ IMPORTANT

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Exam Subject updated successfully'
            )
            return redirect('exams_subject')
    else:
        form = add_exam_subjectmap_form(instance=data)
        form.fields['exname'].queryset = exms   # ✅ IMPORTANT

    return render(
        request,
        'exams/update_exam_subject.html',
        {
            'form': form,
            'skool': sdata,
            'year': year,
            'subj': subj
        }
    )


def clone_exam_subject(request, exam_subject_id):

    sch_id = request.session.get('sch_id')
    sdata = get_object_or_404(school, pk=sch_id)

    yr = get_object_or_404(currentacademicyr, school_name=sdata)
    year = get_object_or_404(academicyr, acad_year=yr, school_name=sdata)

    original = get_object_or_404(
        exam_subjectmap,
        pk=exam_subject_id,
        exname__exam_school=sdata   # 🔐 safety
    )

    subj = subjects.objects.filter(
        subject_class=original.exname.exam_class,
        subject_year=year
    )

    exms = exams.objects.filter(exam_school=sdata,exam_year=year,exam_class=original.exname.exam_class)

    if request.method == 'POST':
        # ❗ NO instance → creates NEW record
        form = add_exam_subjectmap_form(request.POST)
        form.fields['exname'].queryset = exms


        if form.is_valid():
            new_obj = form.save(commit=False)
            # If you want to copy something explicitly, do it here
            new_obj.save()

            messages.success(
                request,
                'Exam Subject cloned successfully'
            )
            return redirect('exams_subject')

    else:
        # ✅ Pre-fill form using original object
        form = add_exam_subjectmap_form(instance=original)
        form.fields['exname'].queryset = exms

    return render(
        request,
        'exams/clone_exam_subject.html',  # separate template is better
        {
            'form': form,
            'skool': sdata,
            'year': year,
            'subj': subj,
            'original': original
        }
    )


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
    data = exams.objects.filter(exam_school=sdata,exam_year=year).order_by('-exam_start_date')
    return render(request,'exams/admit_card.html',{'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def generate_admit_card(request,exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    exam_data = exams.objects.get(pk=exam_id)
    secs = section.objects.filter(class_sec_name=exam_data.exam_class)
    ex_sub = exam_subjectmap.objects.filter(exname=exam_data)

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
        else:
            print(form.errors)
    admt = admit_card.objects.filter(exam_label=exam_data)
    return render(request,'exams/generate_admitcard.html',context={'data':admt,'skool':sdata,'year':year,'secs':secs,'exam_id':exam_id})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def update_formset(request,exam_det_id,exam_label_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    test = admit_card.objects.get(pk=exam_det_id)
    subjdata = exam_result.objects.filter(adm_card=test)
    # Use your custom form (exam_resultform) in the formset
    MyModelFormSet = modelformset_factory(
        exam_result,
        form=exam_resultform,
        extra=0
    )

    formset = MyModelFormSet(
        request.POST or None,
        queryset=exam_result.objects.filter(adm_card__examno=test, adm_card__exam_label=test.exam_label)
    )
    for index, form in enumerate(formset):
        if index < subjdata.count():  # Ensures subjdata doesn't exceed the formset length
            form.subb = subjdata[index].exam_sub
    
    if request.method == 'POST':
        
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Mark update successful')
        else:
            messages.error(request, 'Invalid form')

    return render(request, 'exams/update_formset.html', {'formset': formset, 'data': test, 'skool': sdata, 'year': year,'subjdata':subjdata})

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
def print_adm_card(request,exam_no,examdetid):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata)
    adm_data = admit_card.objects.filter(examno=exam_no,exam_label=examdetid)
    adm_data2 = admit_card.objects.filter(examno=exam_no)[:1].get()

    examsub = exam_subjectmap.objects.filter(exname__exam_class=adm_data2.exam_stu.class_name,exname=examdetid).order_by('paper_date')

    adm={
        'data':adm_data,
        'skool':sdata,
        'year':year,
        'examsub':examsub,
    }
    pdf = render_to_pdf('exams/print_adm_card.html',adm )
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def sectionwise_admitcard(request,sec_id,exam_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    exam_data = exams.objects.get(pk=exam_id)
    admt = admit_card.objects.filter(exam_label=exam_data,exam_stu__secs=sec_id).order_by('-exam_stu__gender','exam_stu__first_name')
    secs = section.objects.filter(class_sec_name=exam_data.exam_class)
    return render(request, 'exams/generate_admitcard.html',
                  context={'data': admt, 'skool': sdata, 'year': year,'secs':secs,'exam_id':exam_id})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def bulk_print_result(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    # Create an empty list to store data for all students
    all_student_data = []

    if request.method == 'POST':
        try:
            selcls = request.POST.get('selectcls')
            selsec = request.POST.get('secs')
            cls = sclass.objects.get(pk=selcls)
            stus = students.objects.filter(class_name=cls,secs=selsec)

            for stud in stus:
                cls = sclass.objects.get(name=stud.class_name, school_name=sdata)
                skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
                exm = exams.objects.filter(exam_class=cls,exam_year=year)
                grp = exam_group.objects.filter(exam_group_school=sdata,)
                subj = subjects.objects.filter(subject_class=cls,subject_year=year)
                subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls,exname__exam_year=year)
                media_path = os.path.join(settings.MEDIA_ROOT, str(stud.student_photo))
                data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_stu=stud,adm_card__exam_label__exam_year=year)
                average_marks_by_subject = data.values('exam_sub__exam_subjects').annotate(
                    avg_marks=Avg('obtained_marks'))
                for lxm in exm:
                    fst = lxm.exam_groupby
                    marks_totals = {}
                    if lxm.exam_groupby == fst:
                        for sb in subexmp:
                            tot = 0
                            for dt in data:

                                if sb.exam_subjects.subject_name == dt.exam_sub.exam_subjects.subject_name:
                                    try:
                                        tot = dt.obtained_marks + tot
                                    except:
                                        tot=tot
                            marks_totals[sb.exam_subjects] = tot

                # Access the subject name and average marks in the QuerySet
                for subject_data in average_marks_by_subject:
                    subject_name = subject_data['exam_sub__exam_subjects']
                    average_marks = subject_data['avg_marks']
                    ssb = subjects.objects.get(pk=subject_name)
                    print(f"Subject: {ssb}, Average Marks: {average_marks}")
                all_student_data.append({
                    'data': data,
                    'stud': stud,
                    'exm': exm,
                    'grp':grp,
                    'subj': subj,
                    'skool': sdata,
                    'aavg': average_marks_by_subject,
                    'photourl': media_path,
                    'skoollogo': skoollogo,
                    'totalmarks': marks_totals,
                })

            # Generate the PDF using data for all students
            pdf = render_to_pdf('studentportal/student_bulk_result.html', {'student_data': all_student_data})
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="bulk_result.pdf"'
                return response
            else:
                return HttpResponse("Failed to generate PDF.", status=500)

        except Exception as e:
            error_msg = f'{e}'
            return HttpResponse(error_msg)

def load_term(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    class_id = request.GET.get('Class_Id')
    terms = exam_group.objects.filter(exam_group_school=sdata)
    return render(request, 'exams/selectterm.html', context={'terms': terms})

def list_exam_group(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exam_group.objects.filter(exam_group_school=sdata)

    return render(request,'exams/examgroups.html',context={'data':data,'skool':sdata,'year':year})

def update_exam_group(request,exmgrp_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    examgroup_data = exam_group.objects.get(id=exmgrp_id)
    data = exam_group.objects.filter(exam_group_school=sdata)
    if request.method == 'POST':
        form = exam_groupform(request.POST or None, instance=examgroup_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam Group updated successfully")
            return render(request, 'exams/examgroups.html', context={'form': form, 'skool': sdata, 'year': year,'data':data})
    form = exam_groupform(instance=examgroup_data)
    return render(request,'exams/update_exam_group.html',context={'form':form,'skool':sdata,'year':year})

def load_sect(request):
    class_id = request.GET.get('Class_Id')
    print("classid=",class_id)
    ssection = section.objects.filter(class_sec_name=class_id).order_by('class_sec_name')
    return render(request, 'exams/selectsection.html',context={'ssection': ssection})
def delete_exam_group(request,exmgrp_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = exam_group.objects.get(id=exmgrp_id)
    data.delete()
    messages.success(request,"Exam Group deleted successfully")
    return render(request,'exams/examgroups.html',context={'skool':sdata,'year':year})


def add_exam_group(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    intial_data = {
        'exam_group_school':sdata,
    }
    if request.method == 'POST':
        form = exam_groupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Exam Group added Successfully")
            return redirect('exam_groups')
    form = exam_groupform(initial=intial_data)
    return render(request,'exams/new_exam_group.html',context={'form':form,'skool':sdata,'year':year})

def student_wise_analysis(request):
    sch_id = request.session.get('sch_id')
    sdata = school.objects.get(pk=sch_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    if request.method == 'POST':
        selcls = request.POST.get('selectcls')
        selsec = request.POST.get('secs')
        if not selcls:
            return JsonResponse({"error": "No class selected."}, status=400)

        try:
            cls = sclass.objects.get(pk=selcls)
            stus = students.objects.filter(class_name=selcls,secs=selsec)
            exm = exams.objects.filter(exam_class=cls)
            grp = exam_group.objects.filter(exam_group_school=sdata)
            subj = subjects.objects.filter(subject_class=cls)
            subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)

            predictions = []

            for stud in stus:
                data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_stu=stud)

                improvement = []
                weakness = []
                top_scorer_status =""
                for subject in subj:
                    subject_results = data.filter(exam_sub__exam_subjects=subject)
                    if subject_results.exists():
                        marks = []
                        for result in subject_results:
                            if result.obtained_marks is not None:
                                calculate = (result.obtained_marks/result.exam_sub.max_marks)*100
                                marks.append(calculate)


                        # Predict improvement
                        if len(marks) >= 2:
                            if marks[-1] > marks[0]:
                                improvement.append(subject.subject_name)
                            # Predict weakness
                            if marks[-1] < marks[0]:
                                weakness.append(subject.subject_name)



                        student_name = f"{stud.first_name} {stud.last_name}"
                        if len(marks)!=0:
                            score = sum(marks)/len(marks)


                            if weakness and score < 45:
                                top_scorer_status = "Danger - No Sign of Improvement"

                            if improvement and score > 80:
                                top_scorer_status = "Potential Top Scorer"
                            elif improvement and score > 90:
                                top_scorer_status = "Top Scorer"
                            elif improvement and score < 45:
                                top_scorer_status = "Below Average -Potential"
                            elif score < 45:
                                top_scorer_status = "Below Average- Shows No Improvement"
                            elif improvement and score < 40:
                                top_scorer_status = "Danger-  Shows Improvement"
                            elif score < 40:
                                top_scorer_status = "Danger-  No Improvement"
                            elif improvement and (score > 45 and score < 80):
                                top_scorer_status = "Average - Shows Improvement"
                            else:
                                top_scorer_status = "Average - No Improvement"

                student_name = f"{stud.first_name} {stud.last_name}"
                media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
                student_prediction = {
                    "student_name": student_name,
                    "section":stud.secs.section_name,
                    "admn_no":stud.admn_no,
                    "father_name":stud.father_name,
                    "phone":stud.phone,
                    "gender":stud.gender,
                    "improvement": improvement,
                    "weakness": weakness,
                    "top_scorer_status": top_scorer_status,
                    "photourl":media_path
                }

                predictions.append(student_prediction)

            context = {
                'predictions': predictions,
                'school_name': sdata.name,
                'school_data':sdata,
                'class_name': cls.name,
                'skoollogo':skoollogo,

            }

            return render(request, 'analysis/predictions.html', context)

        except sclass.DoesNotExist:
            return JsonResponse({"error": "Class not found."}, status=404)

        else:
            return JsonResponse({"error": "Invalid request method."}, status=405)


def class_wise_analysis(request):
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return JsonResponse({"error": "School ID not found in session."}, status=400)

    try:
        sdata = school.objects.get(pk=sch_id)
        skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    except school.DoesNotExist:
        return JsonResponse({"error": "School not found."}, status=404)

    try:
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    except currentacademicyr.DoesNotExist:
        return JsonResponse({"error": "Current academic year not found."}, status=404)
    except academicyr.DoesNotExist:
        return JsonResponse({"error": "Academic year not found."}, status=404)

    if request.method == 'POST':
        selcls = request.POST.get('selectcls')
        selsec = request.POST.get('secs')
        if not selcls:
            return JsonResponse({"error": "No class selected."}, status=400)

        try:
            cls = sclass.objects.get(pk=selcls)
            stus = students.objects.filter(class_name=selcls,secs=selsec)
            exm = exams.objects.filter(exam_class=cls)
            grp = exam_group.objects.filter(exam_group_school=sdata)
            subj = subjects.objects.filter(subject_class=cls)
            subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)

            predictions = []

            for stud in stus:
                data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_stu=stud)

                improvement = []
                weakness = []
                top_scorer_status =""
                for subject in subj:
                    subject_results = data.filter(exam_sub__exam_subjects=subject)
                    if subject_results.exists():
                        marks = []
                        for result in subject_results:
                            if result.obtained_marks is not None:
                                calculate = (result.obtained_marks/result.exam_sub.max_marks)*100
                                marks.append(calculate)


                        # Predict improvement
                        if len(marks) >= 2:
                            if marks[-1] > marks[0]:
                                improvement.append(subject.subject_name)
                            # Predict weakness
                            if marks[-1] < marks[0]:
                                weakness.append(subject.subject_name)



                        student_name = f"{stud.first_name} {stud.last_name}"
                        if len(marks)!=0:
                            score = sum(marks)/len(marks)


                            if weakness and score < 45:
                                top_scorer_status = "Danger - No Sign of Improvement"

                            if improvement and score > 80:
                                top_scorer_status = "Potential Top Scorer"
                            elif improvement and score > 90:
                                top_scorer_status = "Top Scorer"
                            elif improvement and score < 45:
                                top_scorer_status = "Below Average -Potential"
                            elif score < 45:
                                top_scorer_status = "Below Average- Shows No Improvement"
                            elif improvement and score < 40:
                                top_scorer_status = "Danger-  Shows Improvement"
                            elif score < 40:
                                top_scorer_status = "Danger-  No Improvement"
                            elif improvement and (score > 45 and score < 80):
                                top_scorer_status = "Average - Shows Improvement"
                            else:
                                top_scorer_status = "Average - No Improvement"

                student_name = f"{stud.first_name} {stud.last_name}"
                media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
                student_prediction = {
                    "student_name": student_name,
                    "section":stud.secs.section_name,
                    "admn_no":stud.admn_no,
                    "father_name":stud.father_name,
                    "phone":stud.phone,
                    "gender":stud.gender,
                    "improvement": improvement,
                    "weakness": weakness,
                    "top_scorer_status": top_scorer_status,
                    "photourl":media_path
                }

                predictions.append(student_prediction)

            context = {
                'predictions': predictions,
                'school_name': sdata.name,
                'school_data':sdata,
                'class_name': cls.name,
                'skoollogo':skoollogo,

            }

            return render(request, 'analysis/classanalysis.html', context)

        except sclass.DoesNotExist:
            return JsonResponse({"error": "Class not found."}, status=404)

        else:
            return JsonResponse({"error": "Invalid request method."}, status=405)


def student_wise_analysispdf(request):
    try:
        sch_id = request.session.get('sch_id')
        sdata = school.objects.get(pk=sch_id)
        skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)

        if request.method == 'POST':
            selcls = request.POST.get('selectcls')
            selsec = request.POST.get('secs')
            cls = sclass.objects.get(pk=selcls)
            stus = students.objects.filter(class_name=selcls, secs=selsec)
            subj = subjects.objects.filter(subject_class=cls)

            predictions = []

            for stud in stus:
                data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_stu=stud)

                improvement = []
                weakness = []
                top_scorer_status = ""

                for subject in subj:
                    subject_results = data.filter(exam_sub__exam_subjects=subject)
                    if subject_results.exists():
                        marks = []
                        for result in subject_results:
                            if result.obtained_marks is not None:
                                calculate = (result.obtained_marks / result.exam_sub.max_marks) * 100
                                marks.append(calculate)

                        if len(marks) >= 2:
                            first_mark, last_mark = marks[0], marks[-1]

                            if last_mark > first_mark and (last_mark - first_mark) >= 5 and last_mark > 45:
                                improvement.append(subject.subject_name)

                            if last_mark < first_mark and (first_mark - last_mark) >= 7 and first_mark > 45:
                                weakness.append(subject.subject_name)
                                
                            if last_mark <=45:
                                weakness.append(subject.subject_name)

                            student_name = f"{stud.first_name} {stud.last_name}"
                            if marks:
                                score = sum(marks) / len(marks)
                                if weakness and score < 45:
                                    top_scorer_status = "*** - No Sign of Improvement"
                                elif improvement and score > 80:
                                    top_scorer_status = "Potential Top Scorer"
                                elif improvement and score > 90:
                                    top_scorer_status = "Top Scorer"
                                elif improvement and score < 45:
                                    top_scorer_status = "Below Average - Potential"
                                elif score < 45:
                                    top_scorer_status = "Below Average - Shows No Improvement"
                                elif improvement and score < 40:
                                    top_scorer_status = "*** - Shows Improvement"
                                elif score < 40:
                                    top_scorer_status = "Danger - No Improvement"
                                elif improvement and 45 < score < 80:
                                    top_scorer_status = "Average - Shows Improvement"
                                else:
                                    top_scorer_status = "Average - No Improvement"

                media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
                student_prediction = {
                    "student_name": student_name,
                    "section": stud.secs.section_name,
                    "admn_no": stud.admn_no,
                    "gender": stud.gender,
                    "improvement": improvement,
                    "weakness": weakness,
                    "top_scorer_status": top_scorer_status,
                    "photourl": media_path
                }
                predictions.append(student_prediction)

            context = {
                'predictions': predictions,
                'school_name': sdata.name,
                'school_data': sdata,
                'class_name': cls.name,
                'skoollogo': skoollogo,
            }
            try:
                pdf = render_to_pdf('analysis/prediction2.html', context)
            except Exception as e:
                error_message = f"{str(e)}"
                return HttpResponse(error_message, status=500)

            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="result.pdf"'
                return response

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message, status=500)


