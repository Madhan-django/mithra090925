from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('portal', login_required(views.portal), name='portal'),
    path('student_fee_invoice', login_required(views.student_fee_invoice), name='student_fee_invoice'),
    path('student_fee_structure', login_required(views.student_fee_structure), name='student_fee_structure'),
    path('student_fee_reciept', login_required(views.student_fee_reciept), name='student_fee_reciept'),
    path('student_homework', login_required(views.student_homework), name='student_homework'),
    path('student_notice', login_required(views.student_notice), name='student_notice'),
    path('student_events', login_required(views.student_events), name='student_events'),
    path('student_book_issued', login_required(views.student_book_issued), name='student_book_issued'),
    path('student_exam_timetable', login_required(views.student_exam_timetable), name='student_exam_timetable'),
    path('student_exam_timetable_exam/<exam_id>', login_required(views.student_exam_timetable_exam), name='student_exam_timetable_exam'),
    path('print_exam_timetable/<exam_id>', login_required(views.print_exam_timetable), name='print_exam_timetable'),
    path('student_admit_card', login_required(views.student_admit_card), name='student_admit_card'),
    path('student_print_admitcard/<exam_label>/<exam_no>/', login_required(views.student_print_admitcard), name='student_print_admitcard'),
    path('student_print_result', login_required(views.student_print_result), name='student_print_result'),
    path('student_exam_result', login_required(views.single_total_result), name='student_exam_result'),
    path('logout_view', login_required(views.logout_view), name='logout_view'),
    path('student_reprint_reciept/<rec_id>', login_required(views.student_reprint_reciept), name='student_reprint_reciept'),
    path('student_html_to_pdf_directly/<rec_id>', login_required(views.student_html_to_pdf_directly), name='student_html_to_pdf_directly'),
]
