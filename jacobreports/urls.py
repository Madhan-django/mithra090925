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
    # CONSOLIDATED REPORT (ALL CLASSES, ONE DATE)
    # =========================================

    path(
        'consolidated/',
        views.consolidated_class_teacher_report,
        name='consolidated_class_teacher_report'
    ),

    # =========================================
    # VIEW REPORT DETAIL
    # =========================================

    path(
        'view/<int:report_id>/',
        views.view_class_teacher_report,
        name='view_class_teacher_report'
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
    # EXPORT & DELETE (BACKUP TO EXCEL)
    # =========================================

    path(
        'export-delete/',
        views.export_and_delete_class_teacher_reports,
        name='export_and_delete_class_teacher_reports'
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
    # INCHARGE REPORT — DETAIL
    # =========================================

    path(
        'incharge/view/<int:report_id>/',
        views.view_incharge_report,
        name='view_incharge_report'
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

    # =========================================
    # CLASS TEACHER MAPPING — MANAGE
    # =========================================

    path(
        'mappings/',
        views.manage_class_teacher_mappings,
        name='manage_class_teacher_mappings'
    ),

    # =========================================
    # CLASS TEACHER MAPPING — DELETE
    # =========================================

    path(
        'mappings/delete/<int:mapping_id>/',
        views.delete_class_teacher_mapping,
        name='delete_class_teacher_mapping'
    ),

    # =========================================
    # INCHARGE MAPPING — MANAGE
    # =========================================

    path(
        'incharge/mappings/',
        views.manage_incharge_mappings,
        name='manage_incharge_mappings'
    ),

    # =========================================
    # INCHARGE MAPPING — DELETE
    # =========================================

    path(
        'incharge/mappings/delete/<int:mapping_id>/',
        views.delete_incharge_mapping,
        name='delete_incharge_mapping'
    ),

    # =========================================
    # PRINCIPAL DAILY LOG — LIST
    # =========================================

    path(
        'principal-log/',
        views.principal_log_list,
        name='principal_log_list'
    ),

    # =========================================
    # PRINCIPAL DAILY LOG — ADD
    # =========================================

    path(
        'principal-log/add/',
        views.add_principal_log_entry,
        name='add_principal_log_entry'
    ),

    # =========================================
    # PRINCIPAL DAILY LOG — EDIT
    # =========================================

    path(
        'principal-log/edit/<int:entry_id>/',
        views.edit_principal_log_entry,
        name='edit_principal_log_entry'
    ),

    # =========================================
    # PRINCIPAL DAILY LOG — DELETE
    # =========================================

    path(
        'principal-log/delete/<int:entry_id>/',
        views.delete_principal_log_entry,
        name='delete_principal_log_entry'
    ),

    # =========================================
    # PRINCIPAL DAILY LOG — PRINT REPORT
    # =========================================

    path(
        'principal-log/report/',
        views.principal_log_report,
        name='principal_log_report'
    ),

    # =========================================
    # PRINCIPAL LOG ENTRY TYPES — MANAGE PAGE
    # =========================================

    path(
        'principal-log/types/',
        views.manage_principal_log_types,
        name='manage_principal_log_types'
    ),

    # =========================================
    # PRINCIPAL LOG ENTRY TYPES — ADD / DELETE
    # =========================================

    path(
        'principal-log/types/add/',
        views.add_principal_log_type,
        name='add_principal_log_type'
    ),

    path(
        'principal-log/types/delete/<int:type_id>/',
        views.delete_principal_log_type,
        name='delete_principal_log_type'
    ),

    # =========================================
    # PRINCIPAL LOG ACCESS — MANAGE
    # =========================================

    path(
        'principal-log/access/',
        views.manage_principal_log_access,
        name='manage_principal_log_access'
    ),

    # =========================================
    # PRINCIPAL LOG ACCESS — REVOKE
    # =========================================

    path(
        'principal-log/access/revoke/<int:mapping_id>/',
        views.revoke_principal_log_access,
        name='revoke_principal_log_access'
    ),

    # =========================================
    # MORNING REPORT — LIST
    # =========================================

    path(
        'morning-report/',
        views.morning_report_list,
        name='morning_report_list'
    ),

    # =========================================
    # MORNING REPORT — ADD
    # =========================================

    path(
        'morning-report/add/',
        views.add_morning_report,
        name='add_morning_report'
    ),

    # =========================================
    # MORNING REPORT — EDIT
    # =========================================

    path(
        'morning-report/edit/<int:report_id>/',
        views.edit_morning_report,
        name='edit_morning_report'
    ),

    # =========================================
    # MORNING REPORT — DETAIL
    # =========================================

    path(
        'morning-report/view/<int:report_id>/',
        views.view_morning_report,
        name='view_morning_report'
    ),

    # =========================================
    # MORNING REPORT — DELETE
    # =========================================

    path(
        'morning-report/delete/<int:report_id>/',
        views.delete_morning_report,
        name='delete_morning_report'
    ),

    # =========================================
    # MORNING REPORT — PDF
    # =========================================

    path(
        'morning-report/pdf/<int:report_id>/',
        views.morning_report_pdf,
        name='morning_report_pdf'
    ),

]