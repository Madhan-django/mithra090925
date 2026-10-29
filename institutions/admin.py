from django.contrib import admin
from .models import school, SchoolMenuPermission, GroupMenuPermission


class SchoolMenuPermissionInline(admin.StackedInline):
    model = SchoolMenuPermission
    can_delete = False
    verbose_name_plural = "Menu Permissions"


@admin.register(school)
class SchoolAdmin(admin.ModelAdmin):
    inlines = [SchoolMenuPermissionInline]


@admin.register(SchoolMenuPermission)
class SchoolMenuPermissionAdmin(admin.ModelAdmin):
    list_display = ['school', 'admission', 'students', 'staffs', 'academics',
                    'timetable', 'finance', 'payroll', 'transport', 'hostel',
                    'petty_cash', 'examination', 'question_bank', 'library',
                    'assets', 'inventory', 'visitors', 'reports', 'jacob_reports',
                    'certificates']
    list_editable = ['admission', 'students', 'staffs', 'academics',
                     'timetable', 'finance', 'payroll', 'transport', 'hostel',
                     'petty_cash', 'examination', 'question_bank', 'library',
                     'assets', 'inventory', 'visitors', 'reports', 'jacob_reports',
                     'certificates']


@admin.register(GroupMenuPermission)
class GroupMenuPermissionAdmin(admin.ModelAdmin):
    list_display = ['group', 'school', 'admission', 'students', 'staffs',
                    'finance', 'payroll', 'transport', 'hostel', 'configurations',
                    'reports', 'jacob_reports', 'certificates']
    list_filter  = ['school', 'group']
    list_editable = ['admission', 'students', 'staffs',
                     'finance', 'payroll', 'transport', 'hostel',
                     'configurations', 'reports', 'jacob_reports', 'certificates']
