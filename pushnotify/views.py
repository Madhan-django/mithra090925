from django.shortcuts import render, HttpResponse,redirect
from django.core.paginator import Paginator
from .models import GeneralNotification,SectionwiseNotification,SchoolNotification,temp_GeneralNotification
from institutions.models import school
from setup.models import academicyr, currentacademicyr,sclass,section
from admission.models import students
from .forms import New_General_Notification
from mobi.models import DeviceFCMToken
from staff.models import staff
from firebase_admin import messaging
from django_q.models import Schedule
from datetime import datetime, time
from django.utils.dateparse import parse_datetime
from django.utils import timezone

# Create your views here.


def get_page_range(page_obj, window=5):
    current = page_obj.number
    total = page_obj.paginator.num_pages
    start = max(current - window, 1)
    end = min(current + window, total)
    return range(start, end + 1)

def notificationlist(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)

    data = GeneralNotification.objects.filter(Notification_school=sdata).order_by('-create_date')
    bulk_notifications = SectionwiseNotification.objects.filter(Notification_school=sdata).order_by('-id')
    broadcast = SchoolNotification.objects.filter(Notification_school=sdata).order_by('-id')

    paginator1 = Paginator(data, 10)
    paginator2 = Paginator(bulk_notifications, 10)
    paginator3 = Paginator(broadcast, 10)

    page_number1 = request.GET.get("page1")
    page_number2 = request.GET.get("page2")
    page_number3 = request.GET.get("page3")

    page_obj1 = paginator1.get_page(page_number1)
    page_obj2 = paginator2.get_page(page_number2)
    page_obj3 = paginator3.get_page(page_number3)

    return render(
        request,
        "messages/messageslist.html",
        {
            "data": page_obj1,
            "bulk_notifications": page_obj2,
            "broadcast": page_obj3,
            "page_range1": get_page_range(page_obj1),
            "page_range2": get_page_range(page_obj2),
            "page_range3": get_page_range(page_obj3),
            "skool": sdata,
            "year": year,
        },
    )

def notificationlist_copy(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)

    # Querysets
    data = GeneralNotification.objects.filter(Notification_school=sdata).order_by('-create_date')
    bulk_notifications = SectionwiseNotification.objects.filter(Notification_school=sdata).order_by('-id')
    broadcast = SchoolNotification.objects.filter(Notification_school=sdata).order_by('-id')

    # Paginate - 10 per page
    paginator1 = Paginator(data, 10)
    paginator2 = Paginator(bulk_notifications, 10)
    paginator3 = Paginator(broadcast, 10)

    # Get page numbers (different GET params for each table)
    page_number1 = request.GET.get("page1")
    page_number2 = request.GET.get("page2")
    page_number3 = request.GET.get("page3")

    page_obj1 = paginator1.get_page(page_number1)
    page_obj2 = paginator2.get_page(page_number2)
    page_obj3 = paginator3.get_page(page_number3)

    return render(
        request,
        "messages/messageslist.html",
        {
            "data": page_obj1,
            "bulk_notifications": page_obj2,
            "broadcast": page_obj3,
            "skool": sdata,
            "year": year,
        },
    )
    
    
def new_notify(request):
    if 'sch_id' in request.session:
        sch_id = request.session['sch_id']
        sdata = school.objects.get(pk=sch_id)
        year = currentacademicyr.objects.get(school_name=sch_id)
        ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
        data = students.objects.filter(school_student=sdata, ac_year=ayear, student_status='Active')
        staf = request.user.username
        logo = "https://mithran.co.in/media/" + str(sdata.logo)
        cls= sclass.objects.filter(school_name=sdata,acad_year=year)
        try:
            stf = staff.objects.get(staff_user__username=staf)

        except staff.DoesNotExist:
            stf = staff.objects.first()

        initial_value = {
            'created_by_id': stf,
            'is_read': 'NO',
            'status': 'Active',
            'Notification_school': sdata,

        }

        if request.method == 'POST':
            form = New_General_Notification(request.POST)
            if form.is_valid():
                title_msg = form.cleaned_data['title']
                message_cont = form.cleaned_data['message']
                clients = form.cleaned_data['post_to']
                Notif_status = form.cleaned_data['status']
                post_date = form.cleaned_data['post_date']
                success_count = 0
                total_count = clients.count()
                instance =form.save()
                rec_id = instance.id
                client_ids = list(clients.values_list('id', flat=True))

                Schedule.objects.create(
                    func='pushnotify.tasks.send_notification',
                    schedule_type=Schedule.ONCE,
                    next_run=post_date,
                    args=[rec_id]
                )
                return redirect('list_pushMessages')
            else:
                return HttpResponse(f"Form Invalid: {form.errors}")
        else:
            form = New_General_Notification(initial=initial_value)
            return render(request, 'messages/New_Notification.html', {'form': form, 'data': data, 'stf': stf,'skool':sdata,'year':year,
                                                                      'cls':cls})




def ajax_push_load_section(request):
    class_id = request.GET.get('Class_Id')
    print("ssssssssssssssss got section",class_id)
    ssection = section.objects.filter(class_sec_name=class_id).order_by('class_sec_name')
    return render(request, 'students/selectsection.html',context={'ssection': ssection})
    
    
    


def sectionwise_notify(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    # Fix academic year lookup
    year = currentacademicyr.objects.get(school_name=sdata)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=year)

    staf_username = request.user.username
    try:
        stf = staff.objects.get(staff_user__username=staf_username)
    except staff.DoesNotExist:
        # fallback staff if not found
        stf = staff.objects.get(id=1)

    if request.method == "POST":
        aclass = request.POST.get("aclass")
        sect = request.POST.get("sec")
        create_date = request.POST.get("create_date")
        post_date = request.POST.get("post_date")
        title_msg = request.POST.get("title")
        message_cont = request.POST.get("message")

        try:
            cls_obj = sclass.objects.get(id=aclass)
            sec_obj = section.objects.get(id=sect)
        except (sclass.DoesNotExist, section.DoesNotExist):
            return HttpResponse("Invalid class or section", status=400)

        # Save only the template notification
        frm = SectionwiseNotification.objects.create(
            title_msg=title_msg,
            message_cont=message_cont,   # e.g. "Hello {{student_name}}, your class is {{class_name}}"
            aclass=cls_obj,
            ssec=sec_obj,
            create_date=create_date,
            post_date=post_date,
            created_by=stf,
            status='Active',
            Notification_school=sdata,
            success_count=0,
            total_count=0
        )

        # (Optional) If you want to PRE-CREATE notifications here (instead of task)
        temp = 0
        studs = students.objects.filter(class_name=cls_obj, secs=sec_obj, ac_year=ayear)
        for stud in studs:
            gn = GeneralNotification.objects.create(
                title=title_msg,
                message=message_cont,
                create_date=create_date,
                post_date=post_date,
                created_by_id=stf,
                is_read=False,
                status='Active',
                Notification_school=sdata,
                success_count=temp,
                total_count=temp
            )
            gn.post_to.add(stud)  # ✅ fix for ManyToMany
            temp += 1

        rec_id = frm.id

        # Schedule personalized delivery (task will handle push notification later)
        Schedule.objects.create(
            func='pushnotify.tasks.sec_send_notification',
            schedule_type=Schedule.ONCE,
            next_run=post_date if post_date else timezone.now(),
            args=[rec_id]
        )

        return redirect('list_pushMessages')

    # GET request
    return render(
        request,
        'messages/class_sec_messages.html',
        context={'skool': sdata, 'cls': cls, 'year': year}
    )






def school_notify(request):

    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata, acad_year=year)

    staf = request.user.username

    try:
        stf = staff.objects.get(staff_user__username=staf)
    except staff.DoesNotExist:
        stf = staff.objects.first()

    if request.method == "POST":

        title_msg = request.POST.get("title")
        message_cont = request.POST.get("message")

        create_date = timezone.now()

        post_date_str = request.POST.get("post_date")
        post_date = parse_datetime(post_date_str)

        # ⚠️ Ensure timezone-aware datetime
        if timezone.is_naive(post_date):
            post_date = timezone.make_aware(post_date)

        # ✅ Create notification in PENDING state
        frm = SchoolNotification.objects.create(
            title_msg=title_msg,
            message_cont=message_cont,
            create_date=create_date,
            post_date=post_date,
            created_by=stf,
            status='PENDING',   # 🔥 IMPORTANT
            Notification_school=sdata,
            success_count=0,
            total_count=0
        )

        # 🛡️ Avoid duplicate schedules
        Schedule.objects.create(
            func='pushnotify.tasks.school_send_notification',
            schedule_type=Schedule.ONCE,
            next_run=post_date,
            args=[frm.id],
            repeats=1
        )

        return redirect('list_pushMessages')

    return render(
        request,
        'messages/school_messages.html',
        {
            'skool': sdata,
            'cls': cls,
            'year': year,
        }
    )

    
# def school_notify(request):
#     sch_id = request.session['sch_id']
#     sdata = school.objects.get(pk=sch_id)
#     year = currentacademicyr.objects.get(school_name=sch_id)
#     ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
#     cls = sclass.objects.filter(school_name=sdata,acad_year=year)
#     staf = request.user.username
#     success_cnt = 0
#     total_cnt = 0
#     try:
#         stf = staff.objects.get(staff_user__username=staf)
#
#     except staff.DoesNotExist:
#         stf = staff.objects.first()
#     if request.method == "POST":
#         create_date = request.POST.get("create_date")
#         post_date = request.POST.get("post_date")
#         title_msg = request.POST.get("title")
#         message_cont = request.POST.get("message")
#
#         frm = SchoolNotification.objects.create(
#             title_msg= title_msg,message_cont=message_cont,create_date=create_date,post_date=post_date,
#             created_by=stf,status='Active',Notification_school=sdata,success_count=success_cnt,
#             total_count=total_cnt
#         )
#         rec_id = frm.id
#         Schedule.objects.create(
#             func='pushnotify.tasks.school_send_notification',
#             schedule_type=Schedule.ONCE,
#             next_run=post_date,
#             args=[rec_id]
#         )
#         return redirect('list_pushMessages')
#
#     return render(request,'messages/school_messages.html',context={'skool':sdata,'cls':cls,'year':year,'form':form})

def notification(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    cls = sclass.objects.filter(school_name=sdata,acad_year=year)
    staf = request.user.username
    data = students.objects.filter(school_student=sdata, ac_year=ayear, student_status='Active')
    try:
        stf = staff.objects.get(staff_user__username=staf)
    except staff.DoesNotExist:
        stf = staff.objects.first()

    initial_value = {
        'created_by': stf,
        'is_read': 'NO',
        'status': 'Active',
        'Notification_school': sdata,

    }
    form = New_General_Notification(initial=initial_value)
    return render(request, 'messages/New_Notification.html', context={'skool': sdata, 'cls': cls, 'year': year,'form':form,'data': data})
    
    
def sectionwise_notifylist(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = SectionwiseNotification.objects.filter(Notification_school=sdata).order_by('-post_date')
    return render(request,'messages/class_messageslist.html',context={'data':data,'skool':sdata,'year':year})

def school_notifylist(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)
    data = SchoolNotification.objects.filter(Notification_school=sdata).order_by('-post_date')
    return render(request,'messages/school_messageslist.html',context={'data':data,'skool':sdata,'year':year})
    
    
def sectionwise_notify_manual(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year, school_name=sdata)

    msgs = SectionwiseNotification.objects.filter(Notification_school=sdata)
    for msg in msgs:
        studs = students.objects.filter(class_name=msg.aclass, secs=msg.ssec, ac_year=ayear)
        temp1 = 0
        temp2 = 0
        for stud in studs:
            gn = GeneralNotification.objects.create(
                title=msg.title_msg,
                message=msg.message_cont,
                create_date=msg.create_date,
                post_date=msg.post_date,
                created_by_id=msg.created_by,
                is_read=False,
                status='Active',
                Notification_school=sdata,
                success_count=temp1,
                total_count=temp2
            )
            # Add the student to the many-to-many field
            gn.post_to.add(stud)

            temp1 += 1
            temp2 += 1

    return HttpResponse("Message Copied Successfully")