from django.contrib import admin
from .models import LessonPlan, LessonPlanAssignment


class AssignmentInline(admin.TabularInline):
    model = LessonPlanAssignment
    extra = 0


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ['date', 'period_number', 'cls', 'section', 'subject', 'teacher', 'topic', 'status']
    list_filter = ['status', 'teaching_method', 'school']
    search_fields = ['topic', 'chapter']
    inlines = [AssignmentInline]


@admin.register(LessonPlanAssignment)
class LessonPlanAssignmentAdmin(admin.ModelAdmin):
    list_display = ['lesson_plan', 'title', 'due_date', 'is_given', 'is_corrected', 'notify_sent']
    list_filter = ['is_given', 'is_corrected', 'notify_sent']
