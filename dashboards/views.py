import datetime

from django.shortcuts import render
from django.http import HttpResponse
from admission.models import students,enquiry
from academic.models import noticeboard,events
from institutions.models import school
from setup.models import currentacademicyr,academicyr,sclass,section
from staff.models import staff,staff_attendance
from fees.models import addindfee,fees,fee_reciept
from library.models import books,book_issued
from students.models import attendance
from visitors.models import visitors
from authenticate.decorators import allowed_users
from datetime import date
from django.db.models import Sum
# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def home_dashboard(request):
    try:
        # Initialize variables
        totalfee = 0
        collected_fee = 0
        fee_pend = 0
        tdy_collected_fee = 0
        tdy_paid_cnt = 0

        # Get school data from session
        sch_id = request.session['sch_id']
        sdata = school.objects.get(pk=sch_id)

        # Get academic year data
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)

        # Get today's date
        tdy = datetime.date.today()

        # Get various counts and sums
        stf = staff.objects.filter(staff_school=sdata, status='Active').count()
        stf_present = staff_attendance.objects.filter(staff_school=sdata, attndate=tdy, status='Present').count()
        stf_absent = staff_attendance.objects.filter(staff_school=sdata, attndate=tdy, status='Absent').count()
        birthday = students.objects.filter(dob_date__month=tdy.month, dob_date__day=tdy.day, school_student=sdata)
        birthday_cnt = birthday.count()
        stf_birthday = staff.objects.filter(dob__month=tdy.month, dob__day=tdy.day, staff_school=sdata)
        stf_birthday_cnt = stf_birthday.count()
        studentcount = students.objects.filter(school_student=sdata, student_status='Active').count()
        classescount = sclass.objects.filter(school_name=sdata).count()
        sectioncount = section.objects.filter(school_name=sdata).count()
        staffcount = staff.objects.filter(staff_school=sdata, status='Active').count()
        feestd = addindfee.objects.filter(fee_cat__fees_school=sdata, fee_cat__ac_year=year)
        fee_coll_tdy = fee_reciept.objects.filter(reciept_inv__fee_cat__fees_school=sdata, reciept_date=tdy)
        tdy_paid_cnt = fee_coll_tdy.count()
        feepend = addindfee.objects.filter(fee_cat__fees_school=sdata, fee_cat__ac_year=year).exclude(status='Paid')
        fee_part = addindfee.objects.filter(fee_cat__fees_school=sdata, fee_cat__ac_year=year, status='Partially Paid').count()
        enq = enquiry.objects.filter(school_name=sdata, acad_year=yr).count()
        enq_tdy = enquiry.objects.filter(school_name=sdata, acad_year=yr, enq_date=tdy).count()
        followup = enquiry.objects.filter(school_name=sdata, acad_year=yr, enq_followup=tdy).count()
        bks = books.objects.filter(book_school=sdata).count()
        stud_present = attendance.objects.filter(aclass__school_name=sdata, attndate=tdy, status='Present').count()
        stud_absent = attendance.objects.filter(aclass__school_name=sdata, attndate=tdy, status='Absent').count()
        bks_issued = book_issued.objects.filter(book_title__book_school=sdata).count()
        visit = visitors.objects.filter(check_in_time__date=tdy).count()
        ntboard = noticeboard.objects.filter(notice_school=sdata).order_by('-notice_date')
        eve = events.objects.filter(event_school=sdata, start_date__gt=tdy)

        # Calculate totals
        for fee in feestd:
            totalfee += fee.fee_cat.fee_amount
        for fee in fee_reciept.objects.filter(reciept_inv__fee_cat__fees_school=sdata, reciept_inv__fee_cat__ac_year=year):
            collected_fee += fee.paid_amt
        for fee in feepend:
            fee_pend += fee.due_amt
        for tdycoll in fee_coll_tdy:
            tdy_collected_fee += tdycoll.paid_amt

        # Render the template with context data
        return render(request, 'dashboards/home_dashboard.html', context={
            'studentcount': studentcount, 'classescount': classescount, 'sectioncount': sectioncount,
            'staffcount': staffcount, 'totalfee': totalfee, 'year': year, 'collected_fee': collected_fee, 'fee_pend': fee_pend, 'fee_part': fee_part,
            'enq': enq, 'followup': followup, 'books': bks, 'books_issued': bks_issued, 'present': stud_present, 'absent': stud_absent, 'visit': visit,
            'skool': sdata, 'birthday': birthday, 'stf': stf, 'stf_birthday': stf_birthday, 'birthday_cnt': birthday_cnt, 'stf_present': stf_present,
            'stf_absent': stf_absent, 'stf_birthday_cnt': stf_birthday_cnt, 'tdy_collected_fee': tdy_collected_fee, 'tdy_paid_cnt': tdy_paid_cnt,
            'enq_tdy': enq_tdy, 'ntboard': ntboard, 'tdy': tdy, 'eve': eve
        })

    except Exception as e:
        # Print error and return HttpResponse with error message
        return HttpResponse(f"An error occurred: {e}", status=500)

