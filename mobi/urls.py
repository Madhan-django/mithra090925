from django.urls import path
from .views import login_not_required, StaffAPI
from .views import (studentsapi, homeworkapi, attendanceapi, indfeeApi, noticeboardApi, eventsApi, schoolapi, TimetableAPI,
                    FCMSaveApi, MessageApi, ExamTimetable, CalendarAbsenteesApi, ResultDownload, VideoGalleryView, SchoolProfileApi,
                    schprofile_list, edit_schprofile, add_schprofile, delete_schprofile,
                    ClassesAPI, SectionsAPI, StudentsAttendanceAPI, SubmitAttendanceAPI, SubjectsAPI, TeacherHomeworkAddAPI, GeneralNotificationAPI,
                    GrievanceAPI,
                    BannerAPI, banner_list, banner_add, banner_edit, banner_delete,
                    PhotoGalleryView, PhotoAlbumView,
                    photo_gallery_list, photo_gallery_add, photo_gallery_edit, photo_gallery_delete,
                    video_gallery_list, video_gallery_add, video_gallery_edit, video_gallery_delete,
                    TransportAPI)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import leave_api

urlpatterns = [
    path('', studentsapi.as_view(), name='mobstudents'),
    path('api/token/', login_not_required(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', login_not_required(TokenRefreshView.as_view()), name='token_refresh'),
    path('homework/', homeworkapi.as_view(), name='hwork'),
    path('attendance/', attendanceapi.as_view(), name='attendance'),
    path('fee/', indfeeApi.as_view(), name='fee'),
    path('noticeboard/', noticeboardApi.as_view(), name='noticeboard'),
    path('school_events/', eventsApi.as_view(), name='school_events'),
    path('school/', schoolapi.as_view(), name='school_api'),
    path('FcmSave/', FCMSaveApi.as_view(), name='FcmSave'),
    path('messages/', MessageApi.as_view(), name='messages'),
    path('exam_timetable/', ExamTimetable.as_view(), name='exam_timetable'),
    path('CalendarAbsentees/', CalendarAbsenteesApi.as_view(), name='CalendarAbsentees'),
    path('ResultDownload/', ResultDownload.as_view(), name='ResultDownload'),
    path('photos/', PhotoGalleryView.as_view(), name='photos'),
    path('photos/album/', PhotoAlbumView.as_view(), name='photo_album'),
    path('videos/', VideoGalleryView.as_view(), name='videos'),
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
    path('teacher/leave/', leave_api.TeacherLeaveAPI.as_view(), name='teacher_leave'),
    path('teacher/leave/<int:pk>/cancel/', leave_api.TeacherLeaveCancelAPI.as_view(), name='teacher_leave_cancel'),

    # ✅ Add these two
    path('teacher/subjects/', SubjectsAPI.as_view(), name='teacher_subjects'),
    path('teacher/homework/', TeacherHomeworkAddAPI.as_view(), name='teacher_homework'),
    path('teacher/StudentNotification/',GeneralNotificationAPI.as_view(),name='StudentNotification'),

    # Transport (parent-facing)
    path('transport/', TransportAPI.as_view(), name='transport_api'),

    # Grievance
    path('grievance/', GrievanceAPI.as_view(), name='grievance_api'),
    path('grievance/<int:pk>/', GrievanceAPI.as_view(), name='grievance_detail_api'),

    path('timetable/', TimetableAPI.as_view(), name='timetable_api'),

    # Banners — mobile API
    path('banners/', BannerAPI.as_view(), name='banner_api'),

    # Banners — admin CRUD
    path('banner-manage/', banner_list, name='banner_list'),
    path('banner-manage/add/', banner_add, name='banner_add'),
    path('banner-manage/<int:pk>/edit/', banner_edit, name='banner_edit'),
    path('banner-manage/<int:pk>/delete/', banner_delete, name='banner_delete'),

    # Photo Gallery — admin CRUD
    path('photo-gallery/', photo_gallery_list, name='photo_gallery_list'),
    path('photo-gallery/add/', photo_gallery_add, name='photo_gallery_add'),
    path('photo-gallery/<int:pk>/edit/', photo_gallery_edit, name='photo_gallery_edit'),
    path('photo-gallery/<int:pk>/delete/', photo_gallery_delete, name='photo_gallery_delete'),

    # Video Gallery — admin CRUD
    path('video-gallery/', video_gallery_list, name='video_gallery_list'),
    path('video-gallery/add/', video_gallery_add, name='video_gallery_add'),
    path('video-gallery/<int:pk>/edit/', video_gallery_edit, name='video_gallery_edit'),
    path('video-gallery/<int:pk>/delete/', video_gallery_delete, name='video_gallery_delete'),

]
