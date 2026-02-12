from django.urls import path
from django.contrib.auth.decorators import login_required
from students import views

urlpatterns = [
    path('students_list/', login_required(views.students_list), name='students_list'),
    path('students_login/', login_required(views.students_login), name='students_login'),
    path('updatestud/<int:stud_id>/', login_required(views.updatestud), name='updatestud'),
    path('delsstud/<int:stud_id>/', login_required(views.dels_stud), name='delsstud'),
    path('deactivate_user/<int:stud_id>/', login_required(views.deactivate_user), name='deactivate_user'),
    path('activate_user/<int:stud_id>/', login_required(views.activate_user), name='activate_user'),
    path('markattendance/', login_required(views.addattendance), name='addattendance'),
    path('markabsent/<int:stud_id>/', login_required(views.markabsent), name='markabsent'),
    path('markpresent/<int:stud_id>/', login_required(views.markpresent), name='markpresent'),
    path('markholiday/', login_required(views.markholiday), name='markholiday'),
    path('markallpresent/', login_required(views.markallpresent), name='markallpresent'),
    path('viewattendance/', login_required(views.viewattendance), name='viewattendance'),
    path('ajax_load_section/', login_required(views.load_section), name='ajax_load_section'),
    path('ajax_load_uclass/', login_required(views.load_uclass), name='ajax_load_uclass'),
    path('students_promote/', login_required(views.students_promote), name='students_promote'),
    path('students_search/', login_required(views.students_search), name='students_search'),
    path('login_search/', login_required(views.login_search), name='login_search'),
    path('transfer_update/<int:stud_id>/', login_required(views.transfer_update), name='transfer_update'),
    path('student_transfer/', login_required(views.student_transfer), name='student_transfer'),
    path('print_students/', login_required(views.print_students), name='print_students'),
    path('student_csv/', login_required(views.student_csv), name='student_csv'),
    path('stud_import_csv/', login_required(views.stud_import_csv), name='stud_import_csv'),
    path('download_csv_template/', login_required(views.download_csv_template), name='download_csv_template'),
    path('ajax_load_section/', login_required(views.load_section), name='ajax_load_section'),
    path('class_sec_search/', login_required(views.class_sec_search), name='class_sec_search'),
    path('student_password_reset/<str:stud_usernm>/', login_required(views.student_password_reset), name='student_password_reset'),
    path('student_password_resetall/', login_required(views.student_password_resetall), name='student_password_resetall'),
    path('ajax_load_subject/', login_required(views.load_subject), name='ajax_load_subject'),
]

