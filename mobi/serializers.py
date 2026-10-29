from django.contrib.auth.models import User
from rest_framework import serializers
from admission.models import students
from setup.models import sclass,section,subjects,academicyr
from staff.models import staff,homework
from students.models import attendance
from fees.models import addindfee,fees
from institutions.models import school
from academic.models import noticeboard,events
from examination.models import exam_subjectmap,exams
from setup.models import subjects
from pushnotify.models import GeneralNotification
from .models import DeviceFCMToken, SchoolProfile, Banner, PhotoGallery, VideoGallery
from timetable.models import Timetable
from mobiplayer.models import Video
from grievance.models import Grievance


class schoolserializer(serializers.ModelSerializer):
    class Meta:
        model = school
        fields = '__all__'


class academicyrserializer(serializers.ModelSerializer):
    class Meta:
        model = academicyr
        fields = '__all__'
class userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

class sclassserializer(serializers.ModelSerializer):
    class Meta:
        model = sclass
        fields = '__all__'

class sectionserializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = '__all__'
class studentserializer(serializers.ModelSerializer):
    school_student = schoolserializer()
    class_name = sclassserializer()
    secs = sectionserializer()
    class Meta:
        model = students
        fields = '__all__'

class subjectserializer(serializers.ModelSerializer):
    class Meta:
        model = subjects
        fields = '__all__'

class staffserializer(serializers.ModelSerializer):
    class Meta:
        model = staff
        fields = '__all__'
class homeworkserializer(serializers.ModelSerializer):
    hclass = sclassserializer()
    secs = sectionserializer()
    subj = subjectserializer()
    created_by = staffserializer()

    class Meta:
        model = homework
        fields = '__all__'

class attendanceserializer(serializers.ModelSerializer):
    aclass = sclassserializer()
    sec = sectionserializer()


    class Meta:
        model = attendance
        fields = '__all__'


class MonthlyAttendanceSerializer(serializers.Serializer):
    month = serializers.CharField()
    attendance_data = serializers.IntegerField()
    absent = serializers.IntegerField()


class feesserializer(serializers.ModelSerializer):
    iclass = sclassserializer()
    fees_school = schoolserializer()
    ac_year = academicyrserializer()
    class Meta:
        model = fees
        fields = '__all__'


class indfeeserializer(serializers.ModelSerializer):
    fee_cat = feesserializer()
    class_name = sclassserializer()
    stud_name = studentserializer()

    class Meta:
        model = addindfee
        fields = '__all__'

class noticeboardserializer(serializers.ModelSerializer):
    notice_school = schoolserializer()
    class Meta:
        model = noticeboard
        fields = '__all__'

class eventsserializer(serializers.ModelSerializer):
    event_school = schoolserializer()
    class Meta:
        model = events
        fields = '__all__'

class DeviceFcmSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceFCMToken
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralNotification
        fields = ['title', 'message', 'create_date']

class subjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = subjects
        fields = '__all__'
class ExSerializer(serializers.ModelSerializer):
    class Meta:
        model = exams
        fields = '__all__'
class ExamSerializer(serializers.ModelSerializer):
    exname = ExSerializer()
    exam_subjects = subjectSerializer()
    class Meta:
        model = exam_subjectmap
        fields = ['exname', 'exam_subjects', 'paper_date', 'start_time', 'end_time', 'room_no']

class attendserialier(serializers.ModelSerializer):
    student_name = studentserializer()
    class Meta:
        model = attendance
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    Vschool = schoolserializer()
    class Meta:
        model = Video
        fields = '__all__'

class _SchoolNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = school
        fields = ['id', 'name']

class SchoolProfileSerializer(serializers.ModelSerializer):
    school_name = _SchoolNameSerializer()

    class Meta:
        model = SchoolProfile
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'link_url', 'display_order']


class GrievanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievance
        fields = [
            'id', 'area_of_complaint', 'aoc_other', 'detail', 'mobile',
            'complaint_date', 'complaint_status', 'action_date',
            'principal_remark', 'concern_person_remark', 'act_details',
            'concern_person_name', 'no_action_taken'
        ]
        read_only_fields = [
            'id', 'complaint_date', 'complaint_status', 'action_date',
            'principal_remark', 'concern_person_remark', 'act_details',
            'concern_person_name', 'no_action_taken'
        ]


class TimetableSerializer(serializers.Serializer):
    day = serializers.CharField(source='timeslot.day')
    period_number = serializers.IntegerField(source='timeslot.period_number')
    subject_name = serializers.CharField(source='subject.subject_name')
    subject_code = serializers.CharField(source='subject.subject_code')
    teacher_name = serializers.SerializerMethodField()

    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}".strip()



class PhotoGallerySerializer(serializers.ModelSerializer):
    Pschool = schoolserializer(read_only=True)

    class Meta:
        model  = PhotoGallery
        fields = ['id', 'PTitle', 'PThumbnail', 'Plink', 'Pdesc', 'Pdate', 'Ppostdate', 'Pschool', 'status']


class VideoGallerySerializer(serializers.ModelSerializer):
    Vschool = schoolserializer(read_only=True)

    class Meta:
        model  = VideoGallery
        fields = ['id', 'VTitle', 'VThumbnail', 'Vlink', 'Vdesc', 'Vdate', 'Vpostdate', 'Vschool', 'status']


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_id   = serializers.IntegerField(source='id')
    student_name = serializers.SerializerMethodField()
    roll_no      = serializers.CharField()
    is_present   = serializers.SerializerMethodField()

    class Meta:
        model  = students
        fields = ['student_id', 'student_name', 'roll_no', 'is_present']

    def get_student_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"   # ✅ matches your model

    def get_is_present(self, obj):
        date   = self.context.get('date')
        aclass = self.context.get('aclass')
        sec    = self.context.get('sec')
        record = attendance.objects.filter(
            student_name=obj,
            attndate=date,
            aclass_id=aclass,
            sec_id=sec
        ).first()
        return (record.status == 'Present') if record else False

