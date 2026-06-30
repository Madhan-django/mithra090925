from django.shortcuts import render, HttpResponse,redirect
from .models import SchoolProfile
from .forms import SchoolProfileForm
from authenticate.decorators import allowed_users
from students.models import attendancegen
from staff.models import temp_homework
from rest_framework.views import APIView
from .serializers import (
    studentserializer, homeworkserializer, attendanceserializer,
    MonthlyAttendanceSerializer, indfeeserializer, noticeboardserializer,
    eventsserializer, DeviceFcmSerializer, MessageSerializer,staffserializer,
    ExamSerializer, attendserialier, VideoSerializer, schoolserializer,SchoolProfileSerializer,sclassserializer,
    sectionserializer,subjectserializer,MessageSerializer
)
from admission.models import students
from institutions.models import school
from setup.models import currentacademicyr, academicyr, sclass, subjects,section
from examination.models import exam_subjectmap, exams, admit_card, exam_result, exam_group
from staff.models import homework,staff
from mobiplayer.models import Video
from .utils import render_to_pdf
from global_login_required import login_not_required
from functools import wraps
from fees.models import addindfee
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from students.models import attendance
from django.db.models import Avg, Sum
from academic.models import noticeboard, events
from .models import DeviceFCMToken
from pushnotify.models import GeneralNotification, SectionwiseNotification
from datetime import time, datetime, timedelta
from django.utils.timezone import localtime
from django_q.models import Schedule
from django.utils import timezone
import calendar
import os

# Create your views here.

class schoolapi(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')


        if username:
            try:
                student = students.objects.get(usernm=username)
                sch = school.objects.get(name=student.school_student)
                serializer = schoolserializer(sch)

                return Response(serializer.data)
            except school.DoesNotExist:
                return Response({"detail": "School not found"})



class studentsapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({"error": "username required"}, status=400)

        try:
            student = students.objects.get(usernm=username)
            serializer = studentserializer(student)

            # Attendance calculation
            records = attendance.objects.filter(student_name=student)
            days = records.count()
            absent = records.filter(status='Absent').count()
            percentage = round(((days - absent) / days) * 100, 2) if days > 0 else 0

            # Homework Count
            today = localdate()
            homewk = homework.objects.filter(
                hclass=student.class_name,
                secs=student.secs,
                homework_date=today
            ).count() if student.class_name and student.secs else 0

            # ✅ Fees Status — fixed both bugs
            fee_sts = addindfee.objects.filter(student_name=student)
            if not fee_sts.exists():
                fee_status = 'No Fees'        # ✅ handles empty case
            elif fee_sts.filter(status='Unpaid').exists():
                fee_status = 'Unpaid'         # ✅ if ANY record is Unpaid → Unpaid
            else:
                fee_status = 'Paid'           # ✅ only Paid if ALL are Paid

            # Merge into student data
            student_data = serializer.data
            student_data['attendance_percentage'] = percentage
            student_data['homewk'] = homewk
            student_data['fee_status'] = fee_status

            return Response(student_data)

        except students.DoesNotExist:
            return Response({"detail": "Student not found"}, status=404)
                

class attendanceapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        try:
            # Using a context manager for better resource handling
            student =students.objects.get(usernm=username)
            # List to store attendance data for each month
            monthly_attendance = []
            year= str(student.ac_year)
            for month in range(1, 13):
                # Filter attendance records for the specified month
                days = attendance.objects.filter(student_name=student, attndate__month=month).count()
                absent = attendance.objects.filter(student_name=student, attndate__month=month,status='Absent').count()

                monthly_attendance.append({
                    'month': calendar.month_name[month],
                    'attendance_data': days,
                    'absent' : absent,
                    })

                # Serialize the attendance data
          
            serializer = MonthlyAttendanceSerializer(monthly_attendance, many=True)


            return Response(serializer.data)
        except :
            return Response({"Attendance not found"})
            
            
class homeworkapis(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        if username:
            try:

                student = students.objects.get(usernm=username)
                homewk = homework.objects.filter(hclass=student.class_name,secs=student.secs).order_by('-id')
                serializer = homeworkserializer(homewk, many=True)

                return Response(serializer.data)

            except homewk.DoesNotExist:
                return Response({"detail": "Student/homework not found"})


class homeworkapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        if username:
            try:
                student = students.objects.get(usernm=username)

                seven_days_ago = timezone.now() - timedelta(days=7)

                homewk = homework.objects.filter(
                    hclass=student.class_name,
                    secs=student.secs,
                    created_at__gte=seven_days_ago  # 👈 your date field here
                ).order_by('-id')

                serializer = homeworkserializer(homewk, many=True)
                return Response(serializer.data)

            except students.DoesNotExist:
                return Response({"detail": "Student not found"}, status=404)

        return Response({"detail": "Username required"}, status=400)




class indfeeApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')


        try:
            # Assuming you want to filter students by the provided username
            student = students.objects.get(usernm=username)
            feelist = addindfee.objects.filter(stud_name=student,fee_cat__ac_year=student.ac_year)
            serializer = indfeeserializer(feelist, many=True)
            return Response(serializer.data)
        except students.DoesNotExist:
            return Response("Student not Found")
        except addindfee.DoesNotExist:
            return Response("Fee not Found")


class noticeboardApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')


        try:
            # Assuming you want to filter students by the provided username
            student = students.objects.get(usernm='2026151999')
            notice = noticeboard.objects.filter(notice_school=student.school_student).order_by('-notice_date')
            serializer = noticeboardserializer(notice, many=True)

            return Response(serializer.data)
        except notice.DoesNotExist:
            return Response("Notice not Found")

class eventsApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        username = request.query_params.get('username')


        try:
            # Assuming you want to filter students by the provided username
            student = students.objects.get(usernm=username)
            school_events = events.objects.filter(event_school=student.school_student).order_by('-post_date')
            serializer = eventsserializer(school_events,many=True)
            return Response(serializer.data)
        except students.DoesNotExist:
            return Response("Student not Found")
        except addindfee.DoesNotExist:
            return Response("Fee not Found")
        
class FCMSaveApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.query_params.get('username')
        firebaseToken = request.data.get('firecmToken')

        if not username or not firebaseToken:
            return Response({"error": "Both username and FCM token are required."}, status=400)

        try:
            # Delete existing tokens for the username only
            DeviceFCMToken.objects.filter(username=username).delete()

            # Create a new device token for this user
            DeviceFCMToken.objects.create(firecmToken=firebaseToken, username=username)

            return Response({"message": "Device FCM Token updated successfully."}, status=200)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)
            
            
class MessageApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        try:
            student = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        # Query notifications linked via ManyToMany
        notifications = GeneralNotification.objects.filter(
            post_to__id=student.id
        ).order_by('-create_date')

        serializer = MessageSerializer(notifications, many=True, context={'student': student})
        return Response(serializer.data)



class MessagesApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        student = students.objects.get(usernm=username)

        notifications = GeneralNotification.objects.filter(post_to=student).order_by('-post_date')
        serializer = MessageSerializer(notifications, many=True, context={'student': student})

        return Response(serializer.data)


class ExamTimetable(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        student = students.objects.get(usernm=username)
        data = admit_card.objects.filter(exam_stu=student)
        exam_list = []
        for dt in data:
            exams = exam_subjectmap.objects.filter(exname__exam_title=dt.exam_label,exname__exam_school=student.school_student).order_by('-paper_date')
            exam_list.extend(exams)

        serializer = ExamSerializer(exam_list, many=True)
        json_data = serializer.data

        return Response(json_data)


class CalendarAbsenteesApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        student = students.objects.get(usernm=username)
        attend = attendance.objects.filter(student_name=student)
        serializer =attendserialier(attend,many=True)
        json_data = serializer.data
        return Response(json_data)


class ResultDownload(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        stud = students.objects.get(usernm=username)
        sdata = school.objects.get(name=stud.school_student)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        cls = sclass.objects.get(name=stud.class_name, school_name=sdata)
        skoollogo = os.path.join('https://mithran.co.in/media/', str(sdata.logo))
        exm = exams.objects.filter(exam_class=cls,exam_year=year)
        subj = subjects.objects.filter(subject_class=cls,subject_year=year)
        subexmp = exam_subjectmap.objects.filter(exname__exam_class=cls)
        media_path = os.path.join('https://mithran.co.in/media/', str(stud.student_photo))
        data = exam_result.objects.filter(adm_card__exam_label__exam_class=cls, adm_card__exam_label__exam_year=year, adm_card__exam_stu=stud).order_by(
            'adm_card__exam_label__exam_start_date')
        average_marks_by_subject = data.values('exam_sub__exam_subjects').annotate(avg_marks=Avg('obtained_marks'))
        exdata = exam_group.objects.filter(exam_group_school=sdata)

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
                subject_exists = exam_subjectmap.objects.filter(exname__exam_class=cls,
                                                                exam_subjects=sb).exists()
                if subject_exists:
                    total_marks = exam_result.objects.filter(exam_sub__exam_subjects__subject_name=sb.subject_name,
                                                             adm_card__exam_label__exam_class=cls,
                                                             adm_card__exam_stu=stud,
                                                             adm_card__exam_label__exm_grp=grp).aggregate(
                        Sum('obtained_marks'))['obtained_marks__sum']

                    marks_total_instance = MarksTotal(exm_group=grp, exam_subjects=sb, total_marks=total_marks)
                    marks_totals.append(marks_total_instance)

        for subject_data in average_marks_by_subject:
            subject_name = subject_data['exam_sub__exam_subjects']
            average_marks = subject_data['avg_marks']
            ssb = subjects.objects.get(pk=subject_name)
            print(f"Subject: {ssb}, Average Marks: {average_marks}")
        edata = {
            'data': data,
            'stud': stud,
            'exm': exm,
            'exdata': exdata,
            'subj': subj,
            'skool': sdata,
            'aavg': average_marks_by_subject,
            'photourl': media_path,
            'skoollogo': skoollogo,
            'totalmarks': marks_totals

        }


        pdf = render_to_pdf('studentportal/mobile_print_result.html', edata)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="result.pdf"'
            return response
        else:
            # Handle the case when PDF generation fails
            return HttpResponse("Failed to generate PDF.", status=500)


class VideoGallery(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self,request):
        username = request.query_params.get('username')
        stud = students.objects.get(usernm=username)
        sdata = school.objects.get(name=stud.school_student)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        videos = Video.objects.filter(Vschool=sdata)
        serializer = VideoSerializer(videos,many=True)
        return Response(serializer.data)


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def schprofile_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = SchoolProfile.objects.filter(school_name=sdata).first()
    return render(request, 'mobi/schprof_list.html', context={
        'skool': sdata, 'year': year, 'data': data
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def add_schprofile(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)

    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.school_name = sdata
            profile.save()
            return redirect('schprofile_list')
    else:
        form = SchoolProfileForm(initial={'school_name': sdata})

    return render(request, 'mobi/schprof_add.html', context={
        'skool': sdata, 'year': year, 'form': form
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def edit_schprofile(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = SchoolProfile.objects.get(school_name=sdata)

    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('schprofile_list')
    else:
        form = SchoolProfileForm(instance=data)

    return render(request, 'mobi/schprof_edit.html', context={
        'skool': sdata, 'year': year, 'form': form, 'data': data
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def delete_schprofile(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = SchoolProfile.objects.get(school_name=sdata)
    data.delete()
    return redirect('schprofile_list')


class SchoolProfileApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        stud = students.objects.get(usernm=username)
        sdata = school.objects.get(name=stud.school_student)
        yr = currentacademicyr.objects.get(school_name=sdata)
        year = academicyr.objects.get(acad_year=yr, school_name=sdata)
        schprof = SchoolProfile.objects.get(school_name=sdata)
        serializer = SchoolProfileSerializer(schprof, many=True)
        return Response(serializer.data)


class StaffAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            stf = staff.objects.get(staff_user=request.user.username)
            serializer = staffserializer(stf)

            return Response(serializer.data)

        except staff.DoesNotExist:
            return Response({"detail": "Staff not found"}, status=404)




class ClassesAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            stf = staff.objects.get(staff_user=request.user)
            classes = sclass.objects.filter(school_name=stf.staff_school)
            serializer = sclassserializer(classes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SectionsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):
        try:
            secs = section.objects.filter(class_sec_name=class_id)
            serializer = sectionserializer(secs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SubjectsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            class_id = request.query_params.get('class_id')
            if not class_id:
                return Response({'error': 'class_id is required'}, status=400)

            stf = staff.objects.get(staff_user=request.user)
            yr = currentacademicyr.objects.get(school_name=stf.staff_school)
            print("llllllllllllllllllllllllllllllll",yr)
            year = academicyr.objects.get(acad_year=yr, school_name=stf.staff_school)
            print("sssssssssssssssssssssssssssssss",year)
            subs = subjects.objects.filter(subject_class=class_id,subject_year=year)

            serializer = subjectserializer(subs, many=True)

            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


class StudentsAttendanceAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id, sec_id, date):
        try:
            studs = students.objects.filter(class_name=class_id, secs=sec_id)

            # Check if attendance already exists for this class/sec/date
            existing = attendance.objects.filter(
                aclass_id=class_id,
                sec_id=sec_id,
                attndate=date
            )

            if not existing.exists():
                # Auto-create attendance as Present for all students
                attendance.objects.bulk_create([
                    attendance(
                        aclass_id=class_id,
                        sec_id=sec_id,
                        attndate=date,
                        student_name=stud,
                        status='Present'
                    )
                    for stud in studs
                ])

            # Now fetch the attendance map (guaranteed to exist)
            attendance_map = {
                a.student_name_id: a.status
                for a in attendance.objects.filter(
                    aclass_id=class_id,
                    sec_id=sec_id,
                    attndate=date
                )
            }

            serializer = studentserializer(studs, many=True)
            data = [dict(s) for s in serializer.data]

            for student in data:
                student['attendance_status'] = attendance_map.get(student['id'], 'Present')

            return Response(data)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

class SubmitAttendanceAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            class_id = request.data.get('class_id')
            sec_id = request.data.get('sec_id')
            date = request.data.get('date')
            att_records = request.data.get('attendance', [])

            aclass_obj = sclass.objects.get(id=class_id)
            sec_obj = section.objects.get(id=sec_id)

            attendancegen.objects.get_or_create(
                aclass=aclass_obj,
                sec=sec_obj,
                attndate=date
            )

            for record in att_records:
                student_obj = students.objects.get(id=record['student_id'])
                attendance.objects.update_or_create(
                    student_name=student_obj,
                    attndate=date,
                    aclass=aclass_obj,
                    sec=sec_obj,
                    defaults={'status': record['status']}  # ✅ was: 'Present' if record['is_present'] else 'Absent'
                )

            return Response({'message': 'Attendance saved successfully'})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)


class TeacherHomeworkAddAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get homework created by this teacher
            teacher = staff.objects.get(staff_user=request.user)
            homeworks = temp_homework.objects.filter(created_by=teacher)
            serializer = homeworkserializer(homeworks, many=True)

            return Response(serializer.data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    def post(self, request):
        try:
            teacher = staff.objects.get(staff_user=request.user)

            class_id    = request.data.get('class_id')
            sec_id      = request.data.get('sec_id')
            subject_id  = request.data.get('subject_id')
            title       = request.data.get('title')
            description = request.data.get('description')
            hw_date     = request.data.get('homework_date')
            sub_date    = request.data.get('submission_date')

            # Validate required fields
            if not all([class_id, sec_id, subject_id, title, description, hw_date, sub_date]):
                return Response({'error': 'All fields are required'}, status=400)

            # Get current academic year
            current_ac = currentacademicyr.objects.first()
            if not current_ac:
                return Response({'error': 'No active academic year found'}, status=400)

            # Get school from teacher
            school_obj = teacher.staff_school

            hw = temp_homework.objects.create(
                title           = title,
                hclass_id       = class_id,
                secs_id         = sec_id,
                subj_id         = subject_id,
                description     = description,
                homework_date   = hw_date,
                submission_date = sub_date,
                created_by      = teacher,
                acad_yr         = current_ac,
                school_homework = school_obj
            )

            return Response({
                'message': 'Homework created successfully',
                'homework_id': hw.id
            }, status=201)

        except staff.DoesNotExist:
            return Response({'error': 'Teacher profile not found'}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)




class GeneralNotificationAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            teacher = staff.objects.get(staff_user=request.user)
            school_obj = teacher.staff_school

            notifications = GeneralNotification.objects.filter(
                Notification_school=school_obj,
                created_by_id=teacher
            ).order_by('-post_date')

            serializer = MessageSerializer(notifications, many=True)
            return Response(serializer.data)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

    def post(self, request):
        try:
            teacher = staff.objects.get(staff_user=request.user)
            school_obj = teacher.staff_school

            title     = request.data.get('title')
            message   = request.data.get('message')
            post_to   = request.data.get('post_to')
            status    = request.data.get('status', 'Active')
            post_date = request.data.get('post_date')

            if not all([title, message, post_to, post_date]):
                return Response({'error': 'title, message, post_to and post_date are required'}, status=400)

            if not isinstance(post_to, list) or len(post_to) == 0:
                return Response({'error': 'post_to must be a non-empty list of student IDs'}, status=400)

            student_qs = students.objects.filter(
                id__in=post_to,
                school_student=school_obj
            )
            if student_qs.count() == 0:
                return Response({'error': 'No valid students found'}, status=400)

            notif = GeneralNotification.objects.create(
                title               = title,
                message             = message,
                status              = status,
                post_date           = post_date,
                create_date         = timezone.now(),
                created_by_id       = teacher,
                is_read             = False,
                Notification_school = school_obj,
            )
            notif.post_to.set(student_qs)
            notif.save()

            Schedule.objects.create(
                func          = 'pushnotify.tasks.send_notification',
                schedule_type = Schedule.ONCE,
                next_run      = post_date,
                args          = [notif.id]
            )

            return Response({
                'message'          : 'Notification scheduled successfully',
                'notification_id'  : notif.id,
                'recipient_count'  : student_qs.count()
            }, status=201)

        except staff.DoesNotExist:
            return Response({'error': 'Teacher profile not found'}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)