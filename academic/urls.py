from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.academic_dashboard), name='academic_dashboard'),
    path('academic_noticeboard', login_required(views.academic_noticeboard), name='academic_noticeboard'),
    path('add_noticeboard', login_required(views.add_noticeboard), name='add_noticeboard'),
    path('update_noticeboard/<notice_id>', login_required(views.update_noticeboard), name='update_noticeboard'),
    path('delete_noticeboard/<notice_id>', login_required(views.delete_noticeboard), name='delete_noticeboard'),
    path('academic_events', login_required(views.academic_events), name='academic_events'),
    path('add_event', login_required(views.add_event), name='add_event'),
    path('update_event/<event_id>', login_required(views.update_event), name='update_event'),
    path('noticeboard_search', login_required(views.noticeboard_search), name='noticeboard_search'),
    path('event_search', login_required(views.event_search), name='event_search'),
]
