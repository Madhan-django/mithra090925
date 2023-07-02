from django.urls import path
from . import views

urlpatterns= [
    path('exam_list',views.exam_list,name='examlist'),
    path('add_exams',views.add_exams,name='add_exams'),
    path('update_exams/<exam_id>',views.update_exams,name='update_exams'),
    path('delete_exams/<exam_id>',views.delete_exams,name='delete_exams'),
    path('exams_subject',views.exams_subject,name='exams_subject'),
    path('add_exam_subject/<exam_id>',views.add_exam_subject,name='add_exam_subject'),
    path('update_exam_subject/<exam_subject_id>',views.update_exam_subject,name='update_exam_subject'),
    path('delete_exam_subject/<exam_subject_id>',views.delete_exam_subject,name='delete_exam_subject'),
    path('admit_card_list',views.admit_card_list,name='admit_card_list'),
    path('generate_admit_card/<exam_id>',views.generate_admit_card,name='generate_admit_card'),
    path('update_formset/<exam_det_id>/<exam_label_id>',views.update_formset,name='update_formset'),
    path('exam_result',views.exam_result_view,name='exam_result'),
    path('exam_result_print/<admit_id>',views.exam_result_print,name='exam_result_print'),
    path('bulk_print_result',views.bulk_print_result,name='bulk_print_result'),
    path('delete_admit_card/<exam_id>',views.delete_admit_card,name='delete_admit_card'),
    path('print_admit_card/<exam_no>',views.print_adm_card,name='print_admit_card'),
]