from django.contrib import admin
from .models import academicyr,currentacademicyr,sclass,receipt_template,section,AppUpdate,StaffAnnouncement

# Register your models here.
admin.site.register(academicyr)
admin.site.register(currentacademicyr)
admin.site.register(sclass)
admin.site.register(receipt_template)


@admin.register(section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'class_sec_name', 'school_name')
    list_filter = ('school_name', 'class_sec_name')


@admin.register(AppUpdate)
class AppUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'date', 'is_active')
    list_filter = ('badge', 'is_active')
    list_editable = ('is_active',)
    ordering = ('-date',)


@admin.register(StaffAnnouncement)
class StaffAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'posted_by', 'created_at', 'expires_on', 'is_active')
    list_filter = ('school', 'is_active')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
