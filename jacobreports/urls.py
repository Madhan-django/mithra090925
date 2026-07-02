from django.urls import path

from . import views


urlpatterns = [

    # =========================================
    # REPORT LIST
    # =========================================

    path(
        '',
        views.class_teacher_report_list,
        name='class_teacher_report_list'
    ),

    # =========================================
    # ADD REPORT
    # =========================================

    path(
        'add/',
        views.add_class_teacher_report,
        name='add_class_teacher_report'
    ),

    # =========================================
    # EDIT REPORT
    # =========================================

    path(
        'edit/<int:report_id>/',
        views.edit_class_teacher_report,
        name='edit_class_teacher_report'
    ),

    # =========================================
    # DELETE REPORT
    # =========================================

    path(
        'delete/<int:report_id>/',
        views.delete_class_teacher_report,
        name='delete_class_teacher_report'
    ),

    # =========================================
    # INCHARGE REPORT — LIST
    # =========================================

    path(
        'incharge/',
        views.incharge_report_list,
        name='incharge_report_list'
    ),

    # =========================================
    # INCHARGE REPORT — ADD
    # =========================================

    path(
        'incharge/add/',
        views.add_incharge_report,
        name='add_incharge_report'
    ),

    # =========================================
    # INCHARGE REPORT — EDIT
    # =========================================

    path(
        'incharge/edit/<int:report_id>/',
        views.edit_incharge_report,
        name='edit_incharge_report'
    ),

    # =========================================
    # INCHARGE REPORT — DELETE
    # =========================================

    path(
        'incharge/delete/<int:report_id>/',
        views.delete_incharge_report,
        name='delete_incharge_report'
    ),

]