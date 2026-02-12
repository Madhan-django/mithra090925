from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns=[
    path('',login_required(views.grievance_list),name='grievance_list'),
    path('new',login_required(views.grievance_create),name='new_grievance'),
    path('grievance_update/<pk>',login_required(views.grievance_update),name='grievance_update'),
    path('grievance_delete/<pk>',login_required(views.grievance_delete),name='grievance_delete'),
    path('ajax/load-students/', views.ajax_load_students, name='ajax_load_students'),
    path('grievance_search/',views.grievance_search,name='grievance_search')
]