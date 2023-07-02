from django.urls import path
from staff import views

urlpatterns=[
    path('stafflist',views.stafflist,name='stafflist'),
    path('add_staff',views.add_staff,name='add_staff'),
    path('staff_update/<staff_id>',views.staff_update,name='staff_update'),
    path('staff_delete/<staff_id>',views.staff_delete, name='staff_delete'),
    path('staff_status/<staff_id>',views.staff_status, name='staff_status'),
    path('staff_csv',views.staff_csv,name='staff_csv'),
    path('print_staff',views.print_staff,name='print_staff'),
    path('add_staff_attendance',views.gen_staff_attendance,name='add_staff_attendance'),
    path('staff_absent/<attn_id>',views.staff_absent,name='staff_absent'),
    path('staff/<attn_id>',views.staff_present,name='staff_present'),
    path('staff_viewattendance',views.staff_viewattendance,name='staff_viewattendance'),
    path('add_homework',views.add_homework,name='add_homework'),
    path('homework',views.homework_view,name='homework'),
    path('update_homework/<homework_id>',views.update_homework,name='update_homework'),
    path('delete_homework/<homework_id>',views.delete_homework,name='delete_homework'),
    path('staff_password_reset',views.staff_password_reset,name='staff_password_reset'),
    path('staff_search',views.staff_search,name='staff_search'),
    path('homework_search',views.homework_search,name='homework_search')

]

