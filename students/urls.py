from django.urls import path
from students import views

urlpatterns =[

path('students_list',views.students_list,name='students_list'),
path('updatestud/<stud_id>',views.updatestud,name='updatestud'),
path('delstud/<stud_id>',views.delstud,name='delstud'),
path('markattendance',views.addattendance,name='addattendance'),
path('markabsent/<stud_id>',views.markabsent,name='markabsent'),
path('markpresent/<stud_id>',views.markpresent,name='markpresent'),
path('markholiday',views.markholiday,name='markholiday'),
path('markallpresent',views.markallpresent,name='markallpresent'),
path('viewattendance',views.viewattendance,name='viewattendance'),
path('ajax_load_section',views.load_section,name='ajax_load_section'),
path('students_promote',views.students_promote,name='students_promote'),
path('students_search',views.students_search,name='students_search'),
path('transfer_update/<stud_id>',views.transfer_update,name='transfer_update'),
path('student_transfer',views.student_transfer,name='student_transfer'),
path('print_students',views.print_students,name='print_students'),
path('student_csv/',views.student_csv, name='student_csv'),
path('stud_import_csv',views.stud_import_csv,name='stud_import_csv'),
path('download_csv_template',views.download_csv_template,name='download_csv_template'),
]