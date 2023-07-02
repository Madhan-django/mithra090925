from django.shortcuts import render,HttpResponse,redirect
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass,subjects
from authenticate.decorators import allowed_users
from admission.models import students
from fees.models import addindfee,fee_reciept
from staff.models import homework
from academic.models import noticeboard,events
from library.models import book_issued
from examination.models import exam_subjectmap,exams,admit_card,exam_result
from .utils import render_to_pdf
from django.contrib.auth import logout


# Create your views here.
@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def dashboard(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    return render(request,'studentportal/dashboard.html',context={'student':stud,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_invoice(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_inv = addindfee.objects.filter(stud_name=stud)
    return render(request, 'studentportal/fee_invoice.html', context={'data':fee_inv,'student': stud, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_structure(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_inv = addindfee.objects.filter(stud_name=stud)
    return render(request, 'studentportal/fee_structure.html',
                  context={'data': fee_inv, 'student': stud, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_fee_reciept(request):
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    fee_rec = fee_reciept.objects.filter(reciept_inv__stud_name=stud)
    return render(request, 'studentportal/fee_reciepts.html',
                  context={'data': fee_rec, 'student': stud, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher','student'])
def student_homework(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = homework.objects.filter(acad_yr=yr,school_homework=sdata).order_by('-homework_date')
    return render(request, 'studentportal/homework.html', context={'data': data, 'skool': sdata, 'year': year,'stu':stu})

@allowed_users(allowed_roles=['superadmin','student'])
def student_notice(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = noticeboard.objects.filter(notice_school=sdata).order_by('-notice_date')
    return render(request,'studentportal/noticeboard.html',context={'data': data, 'skool': sdata, 'year': year,'stu':stu})

@allowed_users(allowed_roles=['superadmin','student'])
def student_events(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.filter(event_school=sdata).order_by('-start_date')
    return render(request, 'studentportal/events.html',
                  context={'data': data, 'skool': sdata, 'year': year, 'stu': stu})

@allowed_users(allowed_roles=['superadmin','student'])
def show_event(request,event_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = events.objects.get(pk=event_id)
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
    return render(request, 'studentportal/book_issued.html', context={'skool': sdata, 'year': year, 'data': data})

@allowed_users(allowed_roles=['superadmin','student'])
def student_exam_timetable(request):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    examdata = exams.objects.filter(exam_class=stu.class_name)
    return render(request,'studentportal/timetable_exam.html',context={'examdata':examdata,'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','student'])
def student_exam_timetable_exam(request,exam_id):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    exam_det = exam_subjectmap.objects.filter(exname=exam_id)
    return render(request,'studentportal/timetable_exam_view.html',context={'exam_det':exam_det,'exam_id':exam_id,'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','student'])
def print_exam_timetable(request,exam_id):
    usr = request.user.username
    stu = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stu.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    exam_details = exam_subjectmap.objects.filter(exname=exam_id)
    print (exam_details)
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
    return render(request,'studentportal/admitcards.html',context={'adm_card':adm_card,'skool':sdata,'year':year})

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

    examsub = exam_subjectmap.objects.filter(exname__exam_class=adm_data2.exam_stu.class_name)

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
    edata = {
        'data': data,
        'stu': stud,
        'exm': exm,
        'subj': subj,
        'skool': sdata
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
    usr = request.user.username
    stud = students.objects.get(usernm=usr)
    sdata = school.objects.get(name=stud.school_student)
    request.session['sch_id'] = sdata.id
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    return render(request,'studentportal/exam_result.html',context={'skool':sdata,'year':year})

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



