from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from .serializers import (studentserializer,homeworkserializer,attendanceserializer,MonthlyAttendanceSerializer,
                          indfeeserializer,noticeboardserializer,eventsserializer,DeviceFcmSerializer,MessageSerializer,
                          ExamSerializer,attendserialier,VideoSerializer,schoolserializer)

from admission.models import students
from institutions.models import school
from setup.models import currentacademicyr,academicyr,sclass,subjects
from examination.models import exam_subjectmap,exams,admit_card,exam_result,exam_group
from staff.models import homework
from mobiplayer.models import Video
from .utils import render_to_pdf
from global_login_required import login_not_required
from functools import wraps
from fees.models import addindfee
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from students.models import attendance
from django.db.models import Avg,Sum
from academic.models import noticeboard,events
from examination.models import admit_card,exam_subjectmap
from .models import DeviceFCMToken
from pushnotify.models import GeneralNotification,SectionwiseNotification
from datetime import time
from django.utils.timezone import localtime
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


        if username:
            try:
                student = students.objects.get(usernm=username)
                serializer = studentserializer(student)

                return Response(serializer.data)
            except students.DoesNotExist:
                return Response({"detail": "Student not found"})
                

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
            
            
class homeworkapi(APIView):

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
                
                
class homeworksapi(APIView):
    print("yahoooooo")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        if not username:
            return Response({"detail": "Username not provided"}, status=400)

        try:
            student = Student.objects.get(usernm=username)
            now = localtime()
            today = now.date()
            cutoff_time = time(21, 40)

            homewk = Homework.objects.filter(hclass=student.class_name,secs=student.secs).order_by('-id')

            if now.time() < cutoff_time:
                homewk = homewk.exclude(homework_date=today)

            homewk = homewk.order_by('-homework_date')
            serializer = HomeworkSerializer(homewk, many=True)
            return Response(serializer.data)

        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)                




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

















