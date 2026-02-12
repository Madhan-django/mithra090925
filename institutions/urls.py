from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from institutions import views

urlpatterns = [
    path('', login_required(views.selectschool), name='select'),
    path('', login_required(views.allschool), name='institutions'),
    path('addschool', login_required(views.addschool), name='addschool'),
    path('sels/<school_id>', login_required(views.schoollist), name='sels'),
    path('updateschool/<sch_id>', login_required(views.updateschool), name='updateschool'),
    path('delschool/<school_id>', login_required(views.delschool), name='delschool'),
    path('conf_school', login_required(views.conf_school), name='conf_school'),
]
