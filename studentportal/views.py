from django.shortcuts import render,redirect
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,subjects
from authenticate.decorators import allowed_users
from admission.models import students
from fees.models import addindfee,fee_reciept
from staff.models import homework
from academic.models import noticeboard,events
from library.models import book_issued
from examination.models import exam_subjectmap,exams,admit_card,exam_result,exam_group
from pushnotify.models import GeneralNotification
from .utils import render_to_pdf
from django.contrib.auth import logout
from django.db.models import Avg
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Sum
import os



# Create your views here.
#@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def dashboard(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    notify= GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    
    return render(request,'studentportal/studentdashboard.html',context={'student':stud,'skool':sdata,'year':year,'skoollogo':skoollogo})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_invoice(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_inv = addindfee.objects.filter(stud_name=stud)
    notify = GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/fee_invoice.html', context={'data':fee_inv,'student': stud, 'skool': sdata, 'year': year,'skoollogo':skoollogo,})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_structure(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_inv = addindfee.objects.filter(stud_name=stud)
    notify = GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/fee_structure.html',
                  context={'data': fee_inv, 'student': stud, 'skool': sdata, 'year': year,'skoollogo':skoollogo})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_reciept(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_rec = fee_reciept.objects.filter(reciept_inv__stud_name=stud)
    notify = GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/fee_reciepts.html',
                  context={'data': fee_rec, 'student': stud, 'skool': sdata, 'year': year,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_homework(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.filter(acad_yr=yr,school_homework=sdata).order_by('-homework_date')
    notify = GeneralNotification.objects.filter(post_to=stu)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/homework.html', context={'data': data,'student':stu, 'skool': sdata, 'year': year,'stu':stu,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def student_notice(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = noticeboard.objects.filter(notice_school=sdata).order_by('-notice_date')
    notify = GeneralNotification.objects.filter(post_to=stu)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request,'studentportal/noticeboard.html',context={'data': data,'student':stu,'skool': sdata, 'year': year,'stu':stu,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def student_events(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.filter(event_school=sdata).order_by('-start_date')
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    notify = GeneralNotification.objects.filter(post_to=stu)
    return render(request, 'studentportal/events.html',
                  context={'data': data,'student':stu,'skool': sdata, 'year': year, 'stu': stu,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def show_event(request,event_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.get(pk=event_id)
    notify = GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'academic/show_event.html', context={ 'skool': sdata, 'year': year,'data':data})

@allowed_users(allowed_roles=['superadmin','student'])
def student_book_issued(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = book_issued.objects.filter(issued_to=stu,status='Issued')
    notify = GeneralNotification.objects.filter(post_to=stu)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/book_issued.html', context={'skool': sdata,'student':stu,'year': year, 'data': data,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def student_exam_timetable(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    examdata = exams.objects.filter(exam_class=stu.class_name)
    notify = GeneralNotification.objects.filter(post_to=stu)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request,'studentportal/timetable_exam.html',context={'examdata':examdata,'student':stu,'skool': sdata, 'year': year,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def student_exam_timetable_exam(request,exam_id):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    exam_det = exam_subjectmap.objects.filter(exname=exam_id)
    notify = GeneralNotification.objects.filter(post_to=stud)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request,'studentportal/timetable_exam_view.html',context={'exam_det':exam_det,'exam_id':exam_id,'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','student'])
def print_exam_timetable(request,exam_id):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    exam_details = exam_subjectmap.objects.filter(exname=exam_id)
    notify = GeneralNotification.objects.filter(post_to=stud)
    exam_dt={
        'exam_det':exam_details
    }
    pdf = render_to_pdf('studentportal/timetable_exam_print.html',exam_dt)
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','student'])
def student_admit_card(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    adm_card = admit_card.objects.filter(exam_stu=stu)
    notify = GeneralNotification.objects.filter(post_to=stu)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request,'studentportal/admitcards.html',context={'adm_card':adm_card,'student':stu,'skool':sdata,'year':year,'skoollogo':skoollogo})

@allowed_users(allowed_roles=['superadmin','student'])
def student_print_admitcard(request,exam_label,exam_no):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    exlab = exams.objects.get(exam_title=exam_label)
    adm_data = admit_card.objects.filter(exam_label=exlab,examno=exam_no)
    adm_data2 = admit_card.objects.filter(examno=exam_no)[:1].get()
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    examsub = exam_subjectmap.objects.filter(exname__exam_class=adm_data2.exam_stu.class_name)
    notify = GeneralNotification.objects.filter(post_to=stud)
    adm = {
        'data': adm_data,
        'skool': sdata,
        'year': year,
        'examsub': examsub,
    }
    pdf = render_to_pdf('exams/print_adm_card.html', adm)
    return HttpResponse(pdf, content_type='application/pdf')

@allowed_users(allowed_roles=['superadmin','student'])
def student_print_result(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.get(name=stud.class_name)
    exm = exams.objects.filter(exam_class=cls)
    subj = subjects.objects.filter(subject_class=cls)
    print('sub:-', subj)
    data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    edata = {
        'data': data,
        'stu': stud,
        'exm': exm,
        'subj': subj,
        'skool': sdata,
     
    }

    pdf = render_to_pdf('studentportal/print_result.html', edata)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bulk_result.pdf"'
        return response
    else:
        # Handle the case when PDF generation fails
        return HttpResponse("Failed to generate PDF.", status=500)

@allowed_users(allowed_roles=['superadmin','student'])
def student_exam_result(request):
    try:
        usr = request.user.username
        stud = students.objects.get(usernm=usr)
        sdata = school.objects.get(name=stud.school_student)
        request.session['sch_id'] = sdata.id
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
        notify = GeneralNotification.objects.filter(post_to=stud)
        return render(request, 'studentportal/exam_result.html', context={'skool': sdata, 'year': year})
    except Exception as e:
        error_msg = f'e'
        return HttpResponse(error_msg)
@allowed_users(allowed_roles=['superadmin','student'])
def logout_view(request):
    logout(request)
    return redirect('login_user')

@allowed_users(allowed_roles=['superadmin','student'])
def student_reprint_reciept(request,rec_id):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = fee_reciept.objects.get(pk=rec_id)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    return render(request, 'studentportal/reciept_show.html', context={'data': rec_data, 'sch_name': sdata})

@allowed_users(allowed_roles=['superadmin','student'])
def student_html_to_pdf_directly(request,rec_id):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = fee_reciept.objects.get(pk=rec_id)
    data = {
        'sch_name':sdata,
        'rec_no':rec_data.reciept_no,
        'rec_date':rec_data.reciept_date,
        'rec_stud':rec_data.reciept_inv.stud_name,
        'rec_inv':rec_data.reciept_inv.fee_cat,
        'rec_total':rec_data.total,
        'rec_paid_amt':rec_data.paid_amt,
        'rec_ptype':rec_data.payment_type,
        'sch_addr':sdata.address,
        'rec_mob':rec_data.reciept_inv.stud_name.phone,
        'rec_admn': rec_data.reciept_inv.stud_name.admn_no,
        'rec_father':rec_data.reciept_inv.stud_name.father_name,
    }
 
    pdf = render_to_pdf('fee/reciept_print.html',data)
    return HttpResponse(pdf, content_type='application/pdf')

def single_print_result(request):
    
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.get(name=stud.class_name, school_name=sdata)
    skoollogo = os.path.join('https://mithran.co.in/media/',str(sdata.logo))
    exm = exams.objects.filter(exam_class=cls)
    subj = subjects.objects.filter(subject_class=cls)
    subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)
    media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
    data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_stu=stud) 
    average_marks_by_subject = data.values('exam_sub__exam_subjects').annotate(avg_marks=Avg('obtained_marks'))
    exgrp = exam_group.objects.filter(exam_group_school=sdata)
    notify = GeneralNotification.objects.filter(post_to=stud)
    
    try:
       for lxm in exgrp:
        ex_group = lxm.exm_group
        marks_totals = {}
        # Assuming subexmp is related to the current lxm
        for sb in subexmp:
            tot = 0

            for dt in data:
               
                # Assuming sb.exam_subjects.subject_name and dt.exam_sub.exam_subjects.subject_name are the names of the subjects
                if sb.exam_subjects.subject_name == dt.exam_sub.exam_subjects.subject_name:
                   tot = dt.obtained_marks + tot
                marks_totals[sb.exam_subjects] = tot
    except Exception as e:
       error_msg = f'{e}'
       return HttpResponse(error_msg)
    # Access the subject name and average marks in the QuerySet
    for subject_data in average_marks_by_subject:
        subject_name = subject_data['exam_sub__exam_subjects']
        average_marks = subject_data['avg_marks']
        ssb = subjects.objects.get(pk=subject_name)
        print(f"Subject: {ssb}, Average Marks: {average_marks}")
    
    edata = {
        'data': data,
        'stud': stud,
        'exm': exm,
        'subj': subj,
        'skool': sdata,
        'aavg': average_marks_by_subject,
        'photourl': media_path,
        'skoollogo':skoollogo,
        'totalmarks':marks_totals

    }
    
    pdf = render_to_pdf('studentportal/student_print_result.html', edata)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'
        return response
    else:
        # Handle the case when PDF generation fails
        return HttpResponse("Failed to generate PDF.", status=500)


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
            cls = sclass.objects.get(pk=selcls)
            stus = students.objects.filter(class_name=cls)

            for stud in stus:
                cls = sclass.objects.get(name=stud.class_name, school_name=sdata)
                skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
                exm = exams.objects.filter(exam_class=cls)
                subj = subjects.objects.filter(subject_class=cls)
                subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)
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
                                    tot = dt.obtained_marks + tot
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
                    'subj': subj,
                    'skool': sdata,
                    'aavg': average_marks_by_subject,
                    'photourl': media_path,
                    'skoollogo': skoollogo,
                })

            # Generate the PDF using data for all students
                pdf = render_to_pdf('studentportal/student_bulk__result.html', {'student_data': all_student_data})
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="bulk_result.pdf"'
                    return response
                else:
                    return HttpResponse("Failed to generate PDF.", status=500)

        except Exception as e:
            error_msg = f'{e}'
            return HttpResponse(error_msg)


def single_total_result(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    cls = sclass.objects.get(name=stud.class_name, school_name=sdata)
    skoollogo = os.path.join('https://mithran.co.in/media/',str(sdata.logo))
    exm = exams.objects.filter(exam_class=cls,exam_year=year)
    subj = subjects.objects.filter(subject_class=cls,subject_year=year)
    subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)
    media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
    data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_label__exam_year=year,adm_card__exam_stu=stud).exclude(obtained_marks=None).order_by('adm_card__exam_label__exam_start_date')
    average_marks_by_subject = data.values('exam_sub__exam_subjects').annotate(avg_marks=Avg('obtained_marks'))
    exdata = exam_group.objects.filter(exam_group_school=sdata)
    notify = GeneralNotification.objects.filter(post_to=stud)
    extitle = []
    extmp=[]
    exgroup =[] 
    excnt=0    
    class extitleinst:
        def __init__(self, exm_title, exmgrp):
            self.exm_title = exm_title
            self.exmgrp = exmgrp

        def __str__(self):
            return str(self.exm_title)

    try:
        for exarry in data:
            # Safely retrieve attributes to avoid potential AttributeError
            tmp = getattr(exarry.adm_card.exam_label, 'exam_title', None)
            exmgrp = getattr(exarry.adm_card.exam_label.exm_grp, 'exm_group', None)

            if tmp and tmp not in extmp:  # Ensure `tmp` is not None and check for duplicates
                tmpinst = extitleinst(tmp, exmgrp)
                extmp.append(tmp)
                extitle.append(tmpinst)

    except Exception as e:
        # Properly format the error message
        err_msg = f"Error occurred: {str(e)}"
        return HttpResponse(err_msg)


    # Taking first element in exam group
    first_element = exam_group.objects.filter(exam_group_school=sdata).first()
    for tit in extitle:

        if tit.exmgrp == first_element.exm_group:
            excnt = excnt+1
            
    if excnt % 2 == 0:
        exmcnt =3
    else:
        exmcnt=2
    for ext in data:

        tmp = ext.adm_card.exam_label.exm_grp.exm_group

        if tmp not in exgroup:
           exgroup.append(tmp) 
    marks_totals = []

    class MarksTotal:
        def __init__(self, exm_group, exam_subjects, total_marks):
            self.exm_group = exm_group
            self.exam_subjects = exam_subjects
            self.total_marks = total_marks
            
            

        def __str__(self):
            return str(self.exm_group)

    for grp in exdata:
        for sb in subj:
            # Check if this subject exists in exam_subjectmap
            if exam_subjectmap.objects.filter(exname__exam_class=cls, exam_subjects=sb).exists():
                # Filter only published exams
                total_marks = (
                    exam_result.objects
                    .filter(
                        exam_sub__exam_subjects__subject_name=sb.subject_name,
                        adm_card__exam_label__exam_class=cls,
                        adm_card__exam_stu=stud,
                        adm_card__exam_label__exm_grp=grp,
                        adm_card__exam_label__published=True  # ✅ add this line
                    )
                    .aggregate(Sum('obtained_marks'))['obtained_marks__sum']
                )

                if total_marks:  # skip if total is None
                    marks_totals.append(MarksTotal(grp, sb, total_marks))

    for subject_data in average_marks_by_subject:
        subject_name = subject_data['exam_sub__exam_subjects']
        average_marks = subject_data['avg_marks']
        ssb = subjects.objects.get(pk=subject_name)
        print(f"Subject: {ssb}, Average Marks: {average_marks}")
    edata = {
        'data': data,
        'stud': stud,
        'exm': exm,
        'exdata':exdata,
        'subj': subj,
        'skool': sdata,
        'aavg': average_marks_by_subject,
        'photourl': media_path,
        'skoollogo': skoollogo,
        'totalmarks': marks_totals,
        'extitle':extitle,
        'exgroup':exgroup,
        'exmcnt':exmcnt

    }

    pdf = render_to_pdf('studentportal/student_print_result.html', edata)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="result.pdf"'
        return response
    else:
        # Handle the case when PDF generation fails
        return HttpResponse("Failed to generate PDF.", status=500)



@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def portal(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    return render(request,'studentportal/portal2/index.html',context={'student':stud,'skool':sdata,'year':year,'skoollogo':skoollogo})


