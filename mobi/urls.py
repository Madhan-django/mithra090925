from django.urls import path
from .views import login_not_required, StaffAPI
from .views import (studentsapi, homeworkapi, attendanceapi, indfeeApi, noticeboardApi, eventsApi,
                    FCMSaveApi, MessageApi, ExamTimetable, CalendarAbsenteesApi, ResultDownload, VideoGallery, SchoolProfileApi,
                    schprofile_list, edit_schprofile, add_schprofile, delete_schprofile,
                    ClassesAPI, SectionsAPI, StudentsAttendanceAPI, SubmitAttendanceAPI,SubjectsAPI,TeacherHomeworkAddAPI,GeneralNotificationAPI)  # ✅ added
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', studentsapi.as_view(), name='mobstudents'),
    path('api/token/', login_not_required(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', login_not_required(TokenRefreshView.as_view()), name='token_refresh'),
    path('homework/', homeworkapi.as_view(), name='hwork'),
    path('attendance/', attendanceapi.as_view(), name='attendance'),
    path('fee/', indfeeApi.as_view(), name='fee'),
    path('noticeboard/', noticeboardApi.as_view(), name='noticeboard'),
    path('events/', eventsApi.as_view(), name='events'),
    path('FcmSave/', FCMSaveApi.as_view(), name='FcmSave'),
    path('messages/', MessageApi.as_view(), name='messages'),
    path('exam_timetable/', ExamTimetable.as_view(), name='exam_timetable'),
    path('CalendarAbsentees/', CalendarAbsenteesApi.as_view(), name='CalendarAbsentees'),
    path('ResultDownload/', ResultDownload.as_view(), name='ResultDownload'),
    path('videos/', VideoGallery.as_view(), name='videos'),
    path('SchoolProfile/', SchoolProfileApi.as_view(), name='SchoolProfile'),
    path('school-profile/', schprofile_list, name='schprofile_list'),
    path('school-profile/edit/', edit_schprofile, name='edit_schprofile'),
    path('school-profile/add/', add_schprofile, name='add_schprofile'),
    path('school-profile/delete/', delete_schprofile, name='delete_schprofile'),
    path('staff_login', StaffAPI.as_view(), name='staff_login'),

    # ── Teacher Attendance APIs ─────────────────────────────────
    path('teacher/classes/', ClassesAPI.as_view(), name='teacher_classes'),
    path('teacher/sections/<int:class_id>/', SectionsAPI.as_view(), name='teacher_sections'),
    path('teacher/students/<int:class_id>/<int:sec_id>/<str:date>/', StudentsAttendanceAPI.as_view(),
         name='teacher_students'),
    path('teacher/attendance/submit/', SubmitAttendanceAPI.as_view(), name='teacher_attendance_submit'),

    # ✅ Add these two
    path('teacher/subjects/', SubjectsAPI.as_view(), name='teacher_subjects'),
    path('teacher/homework/', TeacherHomeworkAddAPI.as_view(), name='teacher_homework'),
    path('teacher/StudentNotification/',GeneralNotificationAPI.as_view(),name='StudentNotification'),
]
