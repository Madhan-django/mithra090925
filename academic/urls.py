from django.urls import path
from . import views

urlpatterns = [
    path('',views.academic_dashboard,name='academic_dashboard'),
    path('academic_noticeboard',views.academic_noticeboard,name='academic_noticeboard'),
    path('add_noticeboard',views.add_noticeboard,name='add_noticeboard'),
    path('update_noticeboard/<notice_id>',views.update_noticeboard,name='update_noticeboard'),
    path('delete_noticeboard/<notice_id>',views.delete_noticeboard,name='delete_noticeboard'),
    path('academic_events',views.academic_events,name='academic_events'),
    path('add_event',views.add_event,name='add_event'),
    path('update_event/<event_id>',views.update_event,name='update_event'),
    path('noticeboard_search',views.noticeboard_search,name='noticeboard_search'),
    path('event_search',views.event_search,name='event_search'),

]