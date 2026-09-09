from django.contrib import admin
from .models import ClassTeacherMapping, ClassTeacherReport, InchargeMapping, PrincipalDailyLog, PrincipalLogAccessMapping


@admin.register(ClassTeacherMapping)
class ClassTeacherMappingAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'incharge', 'class_teacher')
    list_filter = ('school_name', 'incharge')
    search_fields = (
        'incharge__first_name',
        'incharge__last_name',
        'class_teacher__first_name',
        'class_teacher__last_name',
    )


@admin.register(InchargeMapping)
class InchargeMappingAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'supervisor', 'incharge')
    list_filter = ('school_name', 'supervisor')
    search_fields = (
        'supervisor__first_name',
        'supervisor__last_name',
        'incharge__first_name',
        'incharge__last_name',
    )


@admin.register(ClassTeacherReport)
class ClassTeacherReportAdmin(admin.ModelAdmin):
    list_display = (
        'report_date',
        'school_name',
        'class_name',
        'section',
        'report_submitted_by',
    )
    list_filter = ('school_name', 'class_name', 'report_date')
    search_fields = (
        'report_submitted_by__first_name',
        'report_submitted_by__last_name',
    )


@admin.register(PrincipalDailyLog)
class PrincipalDailyLogAdmin(admin.ModelAdmin):
    list_display = ('entry_date', 'school_name', 'entry_type', 'status', 'description')
    list_filter = ('school_name', 'entry_type', 'status', 'entry_date')
    search_fields = ('description',)
    date_hierarchy = 'entry_date'


@admin.register(PrincipalLogAccessMapping)
class PrincipalLogAccessMappingAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'staff_member')
    list_filter = ('school_name',)
    search_fields = ('staff_member__staff_name',)
