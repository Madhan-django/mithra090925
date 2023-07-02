from django.urls import path,include,re_path
from institutions import views

urlpatterns = [
path('',views.selectschool,name='select'),
path('',views.allschool,name='institutions'),
path('addschool',views.addschool,name='addschool'),
path('sel/ <school_id>',views.schoollist,name='sels'),
path('updateschool/<sch_id>',views.updateschool,name='updateschool'),
path('delschool/<school_id>',views.delschool,name='delschool'),
path('conf_school',views.conf_school,name='conf_school'),

    ]