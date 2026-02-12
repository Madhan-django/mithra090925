from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [

    path('',views.view_timetable,name='view_timetable'),
    path('period_list',login_required(views.period_list),name='period_list'),
    path('create_teaching_allocation',login_required(views.create_teaching_allocation),name='create_teaching_allocation'),
    path('generate_timetable',login_required(views.generate_timetable),name='generate_timetable'),
    path('ajax_load-secsub/', login_required(views.load_secsub), name='ajax_load_secsub'),
    path('view_section_timetable/',login_required( views.view_section_timetable), name='view_section_timetable'),
    path('create_timeslot',login_required(views.create_timeslot),name='create_timeslot'),
    path('delete_singleslot/<slot_id>',login_required(views.delete_singleslot),name='delete_singleslot'),
    path('delete_timeslot',login_required(views.delete_timeslot),name='delete_timeslot'),
    path('edit_teaching_allocation/<allocate_id>',login_required(views.edit_teaching_allocation),name='edit_teaching_allocation'),
    path('delete_teaching_allocation/<allocate_id>',login_required(views.delete_teaching_allocation),name='delete_teaching_allocation'),
    path('delete_timetable',login_required(views.delete_timetable),name='delete_timetable'),
    path('export_timetable_excel',login_required(views.export_timetable_excel),name='export_timetable_excel'),
    path('export/pdf/<int:section_id>/',login_required( views.export_pdf), name='export_pdf'),
    path('export/excel/<int:section_id>/',login_required( views.export_excel), name='export_excel'),
    path('school_export_pdf',login_required(views.school_export_pdf),name='school_export_pdf'),
    path('school_export_excel',login_required(views.school_export_excel),name='school_export_excel'),
    path('timetable_check',login_required(views.timetable_check),name='timetable_check'),
    path('timetable_check_pdf',login_required(views.timetable_check_pdf),name='timetable_check_pdf'),
    path('view_teacher_timetable',login_required(views.view_teacher_timetable),name='view_teacher_timetable'),
    path('teacher_timetable_pdf',login_required(views.teacher_timetable_pdf),name='teacher_timetable_pdf'),
    path('teacher_timetable_pdf',login_required(views.teacher_timetable_pdf),name='teacher_timetable_pdf'),
    path('all_teacher_timetable_pdf',login_required(views.all_teacher_timetable_pdf),name='all_teacher_timetable_pdf'),
    path('add_reservation',login_required(views.add_reservation),name='add_reservation'),
    path('edit_reservation/<pk>',login_required(views.edit_reservation),name='edit_reservation'),
    path('delete_reservation/<pk>',login_required(views.delete_reservation),name='delete_reservation')


]

