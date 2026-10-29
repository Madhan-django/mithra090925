from django.contrib import admin
from .models import LessonPlan, LessonPlanTopic, LessonPlanAssignment


class TopicInline(admin.TabularInline):
    model = LessonPlanTopic
    extra = 0


class AssignmentInline(admin.TabularInline):
    model = LessonPlanAssignment
    extra = 0


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display  = ['chapter', 'cls', 'section', 'subject', 'teacher']
    list_filter   = ['school', 'cls']
    search_fields = ['chapter']
    inlines       = [TopicInline, AssignmentInline]


@admin.register(LessonPlanTopic)
class LessonPlanTopicAdmin(admin.ModelAdmin):
    list_display = ['lesson_plan', 'topic', 'date', 'periods_required', 'teaching_method', 'status']
    list_filter  = ['status', 'teaching_method']


@admin.register(LessonPlanAssignment)
class LessonPlanAssignmentAdmin(admin.ModelAdmin):
    list_display = ['lesson_plan', 'title', 'due_date', 'is_given', 'is_corrected', 'notify_sent']
    list_filter  = ['is_given', 'is_corrected', 'notify_sent']
