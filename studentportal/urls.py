from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('student_fee_invoice',views.student_fee_invoice,name='student_fee_invoice'),
    path('student_fee_structure',views.student_fee_structure,name='student_fee_structure'),
    path('student_fee_reciept',views.student_fee_reciept,name='student_fee_reciept'),
    path('student_homework',views.student_homework,name='student_homework'),
    path('student_notice',views.student_notice,name='student_notice'),
    path('student_events',views.student_events,name='student_events'),
    path('student_book_issued',views.student_book_issued,name='student_book_issued'),
    path('student_exam_timetable',views.student_exam_timetable,name='student_exam_timetable'),
    path('student_exam_timetable_exam/<exam_id>',views.student_exam_timetable_exam,name='student_exam_timetable_exam'),
    path('print_exam_timetable/<exam_id>',views.print_exam_timetable,name='print_exam_timetable'),
    path('student_admit_card',views.student_admit_card,name='student_admit_card'),
    path('student_print_admitcard/<exam_label>/<exam_no>/',views.student_print_admitcard,name='student_print_admitcard'),
    path('student_print_result',views.student_print_result,name='student_print_result'),
    path('student_exam_result',views.student_exam_result,name='student_exam_result'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('student_reprint_reciept/<rec_id>',views.student_reprint_reciept,name='student_reprint_reciept'),
    path('student_html_to_pdf_directly/<rec_id>',views.student_html_to_pdf_directly,name='student_html_to_pdf_directly'),


]