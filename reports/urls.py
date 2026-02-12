# reports/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.reports_home), name='reports_home'),
    path('students_summary_xl/', login_required(views.students_summary_xl), name='students_summary_xl'),
    path('staff_summary_xl/',login_required(views.staff_summary_xl),name='staff_summary_xl'),
    path('classwise_summary_xl/',login_required(views.classwise_summary_xl),name='classwise_summary_xl'),
    path('receipt_summary_xl/', login_required(views.receipt_summary_xl), name='receipt_summary_xl'),
    path('fee_paid_summary_xl/', login_required(views.fee_paid_summary_xl), name='fee_paid_summary_xl'),
    path('fee_summary_xl/', login_required(views.fee_summary_xl), name='fee_summary_xl'),
    path('fee_unpaid_summary_xl/', login_required(views.fee_unpaid_summary_xl), name='fee_unpaid_summary_xl'),
    path('classwiseanalysis',login_required(views.classwiseanalysis),name='classwiseanalysis'),
    path('studentwiseanalysis',login_required(views.studentwiseanalysis),name='studentwiseanalysis'),
    path('fee_classwise_xl/',login_required(views.fee_classwise_xl),name='fee_classwise_xl'),
    path('fee_sums_xl/',login_required(views.fee_sums_xl),name='fee_sums_xl'),
    path('librarybooks/',login_required(views.librarybooks),name='librarybooks'),
    path('Exams_sums_xl/',login_required(views.Exams_sums_xl),name='Exams_sums_xl'),
    path('stocks_summmary',login_required(views.stocks_summmary),name='stocks_summmary'),
    path('cashsource_summary_pdf',login_required(views.cashsource_summary_pdf),name='cashsource_summary_pdf'),
    path('PettyCashExpense_summary_pdf',login_required(views.PettyCashExpense_summary_pdf),name='PettyCashExpense_summary_pdf'),
]
