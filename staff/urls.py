from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('stafflist', login_required(views.stafflist), name='stafflist'),
    path('add_staff', login_required(views.add_staff), name='add_staff'),
    path('staff_update/<staff_id>', login_required(views.staff_update), name='staff_update'),
    path('staff_delete/<staff_id>', login_required(views.staff_delete), name='staff_delete'),
    path('staff_status/<staff_id>', login_required(views.staff_status), name='staff_status'),
    path('staff_csv', login_required(views.staff_csv), name='staff_csv'),
    path('staff_import_csv/', login_required(views.staff_import_csv), name='staff_import_csv'),
    path('download_staff_template',login_required(views.download_staff_template),name='download_staff_template'),
    path('print_staff', login_required(views.print_staff), name='print_staff'),
    path('add_staff_attendance', login_required(views.gen_staff_attendance), name='add_staff_attendance'),
    path('staff_absent/<attn_id>', login_required(views.staff_absent), name='staff_absent'),
    path('staff/<attn_id>', login_required(views.staff_present), name='staff_present'),
    path('staff_viewattendance', login_required(views.staff_viewattendance), name='staff_viewattendance'),
    path('add_homework', login_required(views.add_homework), name='add_homework'),
    path('homework', login_required(views.homework_view), name='homework'),
    path('update_homework/<homework_id>', login_required(views.update_homework), name='update_homework'),
    path('delete_homework/<homework_id>', login_required(views.delete_homework), name='delete_homework'),
    path('staff_password_reset', login_required(views.staff_password_reset), name='staff_password_reset'),
    path('staff_search', login_required(views.staff_search), name='staff_search'),
    path('homework_search', login_required(views.homework_search), name='homework_search'),
    path('homework_manual',views.homework_manual,name='homework_manual'),
    path('homeworkreal_view',views.homeworkreal_view,name='homeworkreal_view')
]
