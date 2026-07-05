from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.lesson_plan_list), name='lesson_plan_list'),
    path('create/', login_required(views.lesson_plan_create), name='lesson_plan_create'),
    path('<int:pk>/', login_required(views.lesson_plan_detail), name='lesson_plan_detail'),
    path('<int:pk>/edit/', login_required(views.lesson_plan_edit), name='lesson_plan_edit'),
    path('<int:pk>/delete/', login_required(views.lesson_plan_delete), name='lesson_plan_delete'),
    path('<int:pk>/pdf/', login_required(views.lesson_plan_pdf), name='lesson_plan_pdf'),

    # assignments
    path('assignment/<int:pk>/toggle-given/', login_required(views.toggle_given), name='toggle_given'),
    path('assignment/<int:pk>/toggle-corrected/', login_required(views.toggle_corrected), name='toggle_corrected'),
    path('assignment/<int:pk>/delete/', login_required(views.assignment_delete), name='assignment_delete'),
    path('assignment/<int:pk>/notify-parents/', login_required(views.notify_parents), name='notify_parents_lesson'),

    # Google Drive notes
    path('<int:plan_pk>/notes/upload/', login_required(views.note_upload), name='note_upload'),
    path('notes/<int:pk>/delete/', login_required(views.note_delete), name='note_delete'),

    # Excel import
    path('import/', login_required(views.excel_import), name='excel_import_lesson'),
    path('import/sample/', login_required(views.excel_sample), name='excel_sample_lesson'),

    # AJAX
    path('ajax/sections/', login_required(views.ajax_load_sections), name='lp_ajax_sections'),
    path('ajax/subjects/', login_required(views.ajax_load_subjects), name='lp_ajax_subjects'),

]
