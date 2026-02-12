from django.urls import path
from .views import login_not_required
from .views import (studentsapi,homeworkapi,attendanceapi,indfeeApi,noticeboardApi,eventsApi,
                    FCMSaveApi,MessageApi,ExamTimetable,CalendarAbsenteesApi,ResultDownload,VideoGallery,schoolapi)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('',studentsapi.as_view(),name='mobstudents'),
    path('api/token/', login_not_required(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', login_not_required(TokenRefreshView.as_view()), name='token_refresh'),
    path('homework/',homeworkapi.as_view(),name='hwork'),
    path('attendance/',attendanceapi.as_view(),name='attendance'),
    path('fee/',indfeeApi.as_view(),name='fee'),
    path('noticeboard/',noticeboardApi.as_view(),name='noticeboard'),
    path('school_events/',eventsApi.as_view(),name='school_events'),
    path('FcmSave/',FCMSaveApi.as_view(),name='FcmSave'),
    path('messages/',MessageApi.as_view(),name='messages'),
    path('exam_timetable/',ExamTimetable.as_view(),name='exam_timetable'),
    path('CalendarAbsentees/',CalendarAbsenteesApi.as_view(),name='CalendarAbsentees'),
    path('ResultDownload/',ResultDownload.as_view(),name='ResultDownload'),
    path('videos/',VideoGallery.as_view(),name='videos'),
    path('school/',schoolapi.as_view(),name='school')
        

]
