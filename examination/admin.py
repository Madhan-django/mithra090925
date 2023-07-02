from django.contrib import admin
from .models import exams,exam_subjectmap,admit_card,exam_result

# Register your models here.
admin.site.register(exams)
admin.site.register(exam_subjectmap)
admin.site.register(admit_card)
admin.site.register(exam_result)