from django.urls import path
from django.contrib.auth.decorators import login_required
from setup import views

urlpatterns = [
    path('Academic-year', login_required(views.academicyear), name='academicyr'),
    path('add_acad_yr', login_required(views.add_acad_yr), name='add_acad_yr'),
    path('edit_academic_yr/<acadyr_id>', login_required(views.edit_academic_yr), name='edit_academic_yr'),
    path('update_acad_yr/<acadyr_id>', login_required(views.update_acad_yr), name='update_acad_yr'),
    path('del_acad_yr/<acadyr_id>', login_required(views.del_acad_yr), name='del_acad_yr'),
    path('set_current_yr', login_required(views.current_acad_yr), name='set_current_yr'),
    path('update_acad_yr/<acadyr_id>', login_required(views.update_acad_yr), name='update_acad_yr'),
    path('listclass', login_required(views.listsclass), name='listclass'),
    path('addclass', login_required(views.addclass), name='addclass'),
    path('updateclass/<cls_id>', login_required(views.updateclass), name='updateclass'),
    path('delcls/<cls_id>', login_required(views.delcls), name='delcls'),
    path('listsec', login_required(views.listsec), name='listsec'),
    path('addsec', login_required(views.addsec), name='addsec'),
    path('updatesec/<sec_id>', login_required(views.updatesec), name='updatesec'),
    path('delsec/<sec_id>', login_required(views.delsec), name='delsec'),
    path('ajax_load_section', login_required(views.load_section), name='ajax_load_section'),
    path('addsubject', login_required(views.addsubject), name='addsubject'),
    path('updatesubject/<sublst_id>', login_required(views.updatesubject), name='updatesubject'),
    path('delsub/<sublst_id>', login_required(views.delsubject), name='delsub'),
    path('listsubjects', login_required(views.subjects_list), name='listsubjects'),
    path('add_admin', login_required(views.add_admin), name='add_admin'),
    path('reset_password/<user_nm>', login_required(views.reset_password), name='reset_password'),
    path('add_receipt_template',login_required(views.add_receipt_template),name='add_receipt_template'),
    path('show_receipt_template',login_required(views.show_receipt_template),name='show_receipt_template'),
    path('del_receipt_template/<sublst_id>',login_required(views.del_receipt_template),name='del_receipt_template'),
    path('update_receipt_template/<sublst_id>',login_required(views.update_receipt_template),name='update_receipt_template'),
    path('homeworktime',login_required(views.homeworktime),name='homeworktime'),
    path('add_homeworktime',login_required(views.add_homeworktime),name='add_homeworktime'),
    path('test_delete',login_required(views.test_delete),name='test_delete'),
    path('copysubjects',login_required(views.copysubjects),name='copysubjects')
    
]
