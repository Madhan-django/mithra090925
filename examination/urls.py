from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('exam_list', login_required(views.exam_list), name='examlist'),
    path('add_exams', login_required(views.add_exams), name='add_exams'),
    path('exam_groups',login_required(views.list_exam_group),name='exam_groups'),
    path('add_exam_group',login_required(views.add_exam_group),name='add_exam_group'),
    path('delete_exam_group/<exmgrp_id>',login_required(views.delete_exam_group),name='delete_exam_group'),
    path('update_exam_group/<exmgrp_id>',login_required(views.update_exam_group),name='update_exam_group'),
    path('update_exams/<exam_id>', login_required(views.update_exams), name='update_exams'),
    path('clone_exams/<exam_id>', login_required(views.clone_exams), name='clone_exams'),
    path('delete_exams/<exam_id>', login_required(views.delete_exams), name='delete_exams'),
    path('exams_subject', login_required(views.exams_subject), name='exams_subject'),
    path('add_exam_subject/<exam_id>', login_required(views.add_exam_subject), name='add_exam_subject'),
    path('update_exam_subject/<exam_subject_id>', login_required(views.update_exam_subject), name='update_exam_subject'),
    path('clone_exam_subject/<exam_subject_id>', login_required(views.clone_exam_subject), name='clone_exam_subject'),
    path('delete_exam_subject/<exam_subject_id>', login_required(views.delete_exam_subject), name='delete_exam_subject'),
    path('admit_card_list', login_required(views.admit_card_list), name='admit_card_list'),
    path('generate_admit_card/<exam_id>', login_required(views.generate_admit_card), name='generate_admit_card'),
    path('update_formset/<exam_det_id>/<exam_label_id>', login_required(views.update_formset), name='update_formset'),
    path('exam_result', login_required(views.exam_result_view), name='exam_result'),
    path('exam_result_print/<admit_id>', login_required(views.exam_result_print), name='exam_result_print'),
    path('ajax_load_sect/', login_required(views.load_sect), name='ajax_load_sect'),
    path('bulk_print_result', login_required(views.bulk_print_result), name='bulk_print_result'),
    path('delete_admit_card/<exam_id>', login_required(views.delete_admit_card), name='delete_admit_card'),
    path('print_admit_card/<exam_no>/<int:examdetid>', login_required(views.print_adm_card), name='print_admit_card'),
    path('sectionwise_admitcard/<sec_id>/<exam_id>', login_required(views.sectionwise_admitcard), name='sectionwise_admitcard'),
    path('student_wise_analysis',login_required(views.student_wise_analysispdf),name='student_wise_analysis'),
    path('class_wise_analysis',login_required(views.class_wise_analysis),name='class_wise_analysis'),



]
