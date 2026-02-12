from django.contrib import admin
from .models import exams,exam_subjectmap,admit_card,exam_result,exam_group

# Register your models here.
admin.site.register(exams)
admin.site.register(exam_subjectmap)
admin.site.register(admit_card)
admin.site.register(exam_result)
admin.site.register(exam_group)
