from django.contrib import admin
from .models import exams,exam_subjectmap,admit_card,exam_result,exam_group,GradeScale

# Register your models here.
admin.site.register(exams)
admin.site.register(exam_subjectmap)
admin.site.register(admit_card)
admin.site.register(exam_result)
admin.site.register(exam_group)


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('school', 'grade', 'min_percent', 'max_percent', 'grade_point', 'remark')
    list_filter = ('school',)
    ordering = ('school', '-min_percent')
