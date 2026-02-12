from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns =[
    path('',login_required(views.notificationlist),name='list_pushMessages'),
    path('sectionwise_notifylist',login_required(views.sectionwise_notifylist),name='sectionwise_notifylist'),
    path('school_notifylist',login_required(views.school_notifylist),name='school_notifylist'),
    path('New_Notification',login_required(views.new_notify),name='new_notify'),
    path('sectionwise',login_required(views.sectionwise_notify),name='sectionwise_notify'),
    path('school_notify',login_required(views.school_notify),name='school_notify'),
    path('notification',login_required(views.notification),name='notification'),
    path('ajax_push_load_section',login_required(views.ajax_push_load_section),name='ajax_push_load_section'),
    path('sectionwise_notify_manual/',login_required(views.sectionwise_notify_manual),name='sectionwise_notify_manual')
    
    
    
   
    
    
   

]
