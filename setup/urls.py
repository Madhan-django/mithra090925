from django.urls import path,include,re_path
from setup import views

urlpatterns = [
path('Academic-year',views.academicyear,name='academicyr'),
path('add_acad_yr',views.add_acad_yr,name='add_acad_yr'),
path('edit_academic_yr/<acadyr_id>',views.edit_academic_yr,name='edit_academic_yr'),
path('update_acad_yr/<acadyr_id>',views.update_acad_yr,name='update_acad_yr'),
path('del_acad_yr/<acadyr_id>',views.del_acad_yr,name='del_acad_yr'),
path('set_current_yr',views.current_acad_yr,name='set_current_yr'),
path('update_acad_yr/<acadyr_id>',views.update_acad_yr,name='update_acad_yr'),
path('listclass',views.listsclass,name='listclass'),
path('addclass',views.addclass,name='addclass'),
path('updateclass/<cls_id>',views.updateclass,name='updateclass'),
path('delcls/<cls_id>',views.delcls,name='delcls'),
path('listsec',views.listsec,name='listsec'),
path('addsec',views.addsec,name='addsec'),
path('updatesec/<sec_id>',views.updatesec,name='updatesec'),
path('delsec/<sec_id>',views.delsec,name='delsec'),
path('ajax_load_section',views.load_section,name='ajax_load_section'),
path('addsubject',views.addsubject,name='addsubject'),
path('updatesubject/<sublst_id>',views.updatesubject,name='updatesubject'),
path('delsub/<sublst_id>',views.delsubject,name='delsub'),
path('listsubjects',views.subjects_list,name='listsubjects'),
path('add_admin',views.add_admin,name='add_admin'),
path('reset_password/<user_nm>',views.reset_password,name='reset_password'),


    ]