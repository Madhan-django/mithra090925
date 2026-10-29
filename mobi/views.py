from django.shortcuts import render, HttpResponse,redirect
from .models import SchoolProfile, Banner, PhotoGallery, VideoGallery, GalleryPhoto
VideoGalleryModel = VideoGallery  # alias kept for existing API views
from .forms import SchoolProfileForm, BannerForm, GalleryPhotoForm, PhotoGalleryForm, VideoGalleryForm
from authenticate.decorators import allowed_users
from students.models import attendancegen
from staff.models import temp_homework
from rest_framework.views import APIView
from .serializers import (
    studentserializer, homeworkserializer, attendanceserializer,
    MonthlyAttendanceSerializer, indfeeserializer, noticeboardserializer,
    eventsserializer, DeviceFcmSerializer, MessageSerializer,staffserializer,
    ExamSerializer, attendserialier, VideoSerializer, schoolserializer,SchoolProfileSerializer,sclassserializer,
    sectionserializer,subjectserializer,MessageSerializer,GrievanceSerializer,BannerSerializer,
    TimetableSerializer, PhotoGallerySerializer, VideoGallerySerializer
)
from timetable.models import Timetable
from grievance.models import Grievance
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
from datetime import time, datetime, timedelta, date
from django.db.models import Q
from django.utils.timezone import localtime, localdate
from django_q.models import Schedule
from django.utils import timezone
import calendar
import os
import re
import hashlib
from django.core.cache import cache

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
            fee_sts = addindfee.objects.filter(stud_name=student)
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

            except students.DoesNotExist:
                return Response({"detail": "Student/homework not found"})


class homeworkapi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')

        if username:
            try:
                student = students.objects.get(usernm=username)

                seven_days_ago = date.today() - timedelta(days=7)

                homewk = homework.objects.filter(
                    hclass=student.class_name,
                    secs=student.secs,
                    homework_date__gte=seven_days_ago
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
            student = students.objects.get(usernm=username)
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
        attend = attendance.objects.filter(student_name=student, status='Absent')
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


class PhotoGalleryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)
        photos = PhotoGallery.objects.filter(Pschool=sdata, status='active')
        serializer = PhotoGallerySerializer(photos, many=True)
        data = list(serializer.data)

        # Photos added from Gallery Manage (GalleryPhoto) — same shape as PhotoGallery
        school_data = schoolserializer(sdata).data
        for gp in GalleryPhoto.objects.filter(school=sdata, is_active=True):
            data.append({
                'id': f'g{gp.id}',
                'PTitle': gp.title,
                'PThumbnail': '',
                'Plink': gp.view_url,
                'Pdesc': gp.album,
                'Pdate': None,
                'Ppostdate': gp.created_at.date().isoformat() if gp.created_at else None,
                'Pschool': school_data,
                'status': 'active',
            })

        # No thumbnail (Drive folder / website album / image link) → first image as cover
        for item in data:
            if not item.get('PThumbnail'):
                try:
                    imgs = _album_images(item.get('Plink') or '')
                    if imgs:
                        item['PThumbnail'] = imgs[0]['thumb']
                except Exception as e:
                    print(f"Gallery cover error for {item.get('Plink')}: {e}")
        return Response(data)


# ── Photo album slideshow (Drive folder / website album page) ─────────────

DRIVE_FOLDER_RE = re.compile(r'drive\.google\.com/drive/(?:u/\d+/)?folders/([a-zA-Z0-9_-]+)')
DRIVE_FILE_RE = re.compile(r'drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:export=\w+&)?id=)([a-zA-Z0-9_-]+)')
IMAGE_URL_RE = re.compile(r'\.(?:jpe?g|png|gif|webp|bmp)(?:\?.*)?$', re.IGNORECASE)


def _drive_folder_id(link):
    m = DRIVE_FOLDER_RE.search(link or '')
    return m.group(1) if m else None


def _drive_file_id(link):
    m = DRIVE_FILE_RE.search(link or '')
    return m.group(1) if m else None


def _is_image_url(link):
    return bool(IMAGE_URL_RE.search((link or '').strip()))


def _drive_thumb(file_id, size):
    return f'https://drive.google.com/thumbnail?id={file_id}&sz=w{size}'


def _album_img(img_id, name, thumb, full):
    return {'id': img_id, 'name': name, 'thumb': thumb, 'full': full}


def _album_images(link):
    """
    All photos for a gallery link (cached 10 minutes):
      Drive folder            → every image in the folder
      Drive file / image URL  → that one image
      Website album page /
      web folder listing      → every album image on that page
    Returns [] when nothing is found. Raises only on Drive API errors.
    """
    link = (link or '').strip()
    if not link:
        return []
    key = 'gallery_album_' + hashlib.md5(link.encode('utf-8')).hexdigest()
    images = cache.get(key)
    if images is not None:
        return images

    folder_id = _drive_folder_id(link)
    file_id = _drive_file_id(link)
    if folder_id:
        from lessonplan.drive_utils import list_folder_images
        images = [
            _album_img(f['id'], f.get('name', ''), _drive_thumb(f['id'], 400), _drive_thumb(f['id'], 2048))
            for f in list_folder_images(folder_id)
        ]
    elif file_id:
        images = [_album_img(file_id, '', _drive_thumb(file_id, 400), _drive_thumb(file_id, 2048))]
    elif _is_image_url(link) or not link.startswith('http'):
        images = [_album_img(link, '', link, link)]
    else:
        from .web_album import fetch_album_images
        images = [
            _album_img(u, u.rsplit('/', 1)[-1].split('?')[0], u, u)
            for u in fetch_album_images(link)
        ]

    # empty result cached only 2 minutes so a temporarily-down website is retried soon
    cache.set(key, images, 600 if images else 120)
    return images


class PhotoAlbumView(APIView):
    """
    GET /mobi/photos/album/?username=<usernm>&id=<photo id from /mobi/photos/>
    Returns {"title": ..., "images": [{"id","name","thumb","full"}, ...]}
    If no images can be found: {"title": ..., "images": [], "web_url": <link>} → app opens browser
    id = number  → PhotoGallery
    id = g<num>  → GalleryPhoto (Gallery Manage)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        photo_id = request.query_params.get('id', '')
        if not username or not photo_id:
            return Response({'error': 'username and id required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)

        title, link = '', ''
        if photo_id.startswith('g') and photo_id[1:].isdigit():
            gp = GalleryPhoto.objects.filter(pk=int(photo_id[1:]), school=sdata, is_active=True).first()
            if gp:
                title, link = gp.title, gp.view_url
        elif photo_id.isdigit():
            pg = PhotoGallery.objects.filter(pk=int(photo_id), Pschool=sdata, status='active').first()
            if pg:
                title, link = pg.PTitle, pg.Plink
        if not link:
            return Response({'error': 'Album not found'}, status=404)

        try:
            images = _album_images(link)
        except Exception as e:
            return Response({'error': f'Could not read album: {e}'}, status=502)

        if images:
            return Response({'title': title, 'images': images})
        return Response({'title': title, 'images': [], 'web_url': link})


class VideoGalleryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            stud = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        sdata = school.objects.get(name=stud.school_student)
        videos = VideoGalleryModel.objects.filter(Vschool=sdata, status='active')
        serializer = VideoGallerySerializer(videos, many=True)
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
        schprof = SchoolProfile.objects.filter(school_name=sdata).first()
        if not schprof:
            return Response({"detail": "School profile not found"}, status=404)
        serializer = SchoolProfileSerializer(schprof)
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


class GrievanceAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            student = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        if pk:
            try:
                grievance = Grievance.objects.get(pk=pk, stud_name=student)
                return Response(GrievanceSerializer(grievance).data)
            except Grievance.DoesNotExist:
                return Response({'error': 'Grievance not found'}, status=404)

        grievances = Grievance.objects.filter(stud_name=student).order_by('-complaint_date')
        return Response(GrievanceSerializer(grievances, many=True).data)

    def post(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            student = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        area   = request.data.get('area_of_complaint')
        detail = request.data.get('detail')
        mobile = request.data.get('mobile')

        if not area or not detail or not mobile:
            return Response({'error': 'area_of_complaint, detail and mobile are required'}, status=400)

        sdata = school.objects.get(name=student.school_student)
        yr    = currentacademicyr.objects.get(school_name=sdata)
        year  = academicyr.objects.get(acad_year=yr, school_name=sdata)

        grievance = Grievance.objects.create(
            stud_name=student,
            gschool=sdata,
            gclass=student.class_name,
            gsec=student.secs,
            ac_year=year,
            area_of_complaint=area,
            aoc_other=request.data.get('aoc_other'),
            detail=detail,
            mobile=mobile,
            complaint_date=timezone.now(),
            complaint_status='Open',
            complaint_received='APP',
            act_intimation_to_person='APP',
        )
        return Response(GrievanceSerializer(grievance).data, status=201)




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

# ── Banner API ──────────────────────────────────────────────────────────────

class BannerAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            student = students.objects.get(usernm=username)
            sdata = school.objects.get(name=student.school_student)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
        except school.DoesNotExist:
            return Response({'error': 'School not found'}, status=404)

        today = date.today()
        banners = Banner.objects.filter(
            school_name=sdata,
            is_active=True,
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today)
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=today)
        )
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(serializer.data)


# ── Banner Admin CRUD ───────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def banner_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    banners = Banner.objects.filter(school_name=sdata)
    return render(request, 'mobi/banner_list.html', {'skool': sdata, 'banners': banners})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def banner_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save(commit=False)
            banner.school_name = sdata
            banner.save()
            return redirect('banner_list')
    else:
        form = BannerForm()
    return render(request, 'mobi/banner_add.html', {'skool': sdata, 'form': form})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def banner_edit(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    banner = Banner.objects.get(pk=pk, school_name=sdata)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('banner_list')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'mobi/banner_edit.html', {'skool': sdata, 'form': form, 'banner': banner})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def banner_delete(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    Banner.objects.filter(pk=pk, school_name=sdata).delete()
    return redirect('banner_list')


class TimetableAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'error': 'username required'}, status=400)
        try:
            student = students.objects.get(usernm=username)
        except students.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        if not student.class_name or not student.secs:
            return Response({'error': 'Student has no class/section assigned'}, status=400)

        entries = Timetable.objects.filter(
            section=student.secs,
            timetable_school=student.school_student,
        ).select_related('timeslot', 'subject', 'teacher').order_by(
            'timeslot__day', 'timeslot__period_number'
        )
        serializer = TimetableSerializer(entries, many=True)
        return Response(serializer.data)


# ── Gallery Admin CRUD ──────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gallery_list(request):
    from django.contrib import messages as msg
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    photos = GalleryPhoto.objects.filter(school=sdata)
    albums = photos.values_list('album', flat=True).distinct()
    return render(request, 'mobi/gallery_list.html', {
        'skool': sdata, 'photos': photos, 'albums': [a for a in albums if a]
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gallery_add(request):
    from django.contrib import messages as msg
    from lessonplan.drive_utils import upload_gallery_photo
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    if request.method == 'POST':
        form = GalleryPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            add_type = request.POST.get('_add_type', 'upload')
            title    = form.cleaned_data['title']
            album    = form.cleaned_data.get('album', '')
            is_active = form.cleaned_data.get('is_active', True)
            drive_file_id = ''
            view_url = ''
            if add_type == 'upload' and form.cleaned_data.get('photo'):
                photo_file = form.cleaned_data['photo']
                try:
                    drive_file_id, view_url = upload_gallery_photo(
                        photo_file,
                        photo_file.name,
                        photo_file.content_type,
                        sdata.name,
                        album or 'General',
                    )
                except Exception as e:
                    msg.error(request, f'Drive upload failed: {e}')
                    return render(request, 'mobi/gallery_add.html', {'skool': sdata, 'form': form})
            else:
                view_url = form.cleaned_data.get('link_url', '')
            GalleryPhoto.objects.create(
                title=title, album=album, drive_file_id=drive_file_id,
                view_url=view_url, is_active=is_active, school=sdata
            )
            msg.success(request, 'Photo added to gallery.')
            return redirect('gallery_list')
    else:
        form = GalleryPhotoForm()
    return render(request, 'mobi/gallery_add.html', {'skool': sdata, 'form': form})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gallery_delete(request, pk):
    from lessonplan.drive_utils import delete_note
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    photo = GalleryPhoto.objects.filter(pk=pk, school=sdata).first()
    if photo:
        if photo.drive_file_id:
            delete_note(photo.drive_file_id)
        photo.delete()
    return redirect('gallery_list')


# ── Photo Gallery Admin CRUD ────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def photo_gallery_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    photos = PhotoGallery.objects.filter(Pschool=sdata)
    return render(request, 'mobi/photo_gallery_list.html', {'skool': sdata, 'photos': photos})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def photo_gallery_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    if request.method == 'POST':
        form = PhotoGalleryForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.Pschool = sdata
            photo.save()
            return redirect('photo_gallery_list')
    else:
        form = PhotoGalleryForm()
    return render(request, 'mobi/photo_gallery_form.html', {'skool': sdata, 'form': form, 'action': 'Add'})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def photo_gallery_edit(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    photo = PhotoGallery.objects.get(pk=pk, Pschool=sdata)
    if request.method == 'POST':
        form = PhotoGalleryForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo_gallery_list')
    else:
        form = PhotoGalleryForm(instance=photo)
    return render(request, 'mobi/photo_gallery_form.html', {'skool': sdata, 'form': form, 'action': 'Edit', 'obj': photo})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def photo_gallery_delete(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    PhotoGallery.objects.filter(pk=pk, Pschool=sdata).delete()
    return redirect('photo_gallery_list')


# ── Video Gallery Admin CRUD ────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def video_gallery_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    videos = VideoGallery.objects.filter(Vschool=sdata)
    return render(request, 'mobi/video_gallery_list.html', {'skool': sdata, 'videos': videos})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def video_gallery_add(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    if request.method == 'POST':
        form = VideoGalleryForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.Vschool = sdata
            video.save()
            return redirect('video_gallery_list')
    else:
        form = VideoGalleryForm()
    return render(request, 'mobi/video_gallery_form.html', {'skool': sdata, 'form': form, 'action': 'Add'})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def video_gallery_edit(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    video = VideoGallery.objects.get(pk=pk, Vschool=sdata)
    if request.method == 'POST':
        form = VideoGalleryForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_gallery_list')
    else:
        form = VideoGalleryForm(instance=video)
    return render(request, 'mobi/video_gallery_form.html', {'skool': sdata, 'form': form, 'action': 'Edit', 'obj': video})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def video_gallery_delete(request, pk):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    VideoGallery.objects.filter(pk=pk, Vschool=sdata).delete()
    return redirect('video_gallery_list')

