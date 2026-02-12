from django.contrib import admin
from .models import staff,staff_attendance,homework,temp_homework

# Register your models here.
admin.site.register(staff)
admin.site.register(staff_attendance)
admin.site.register(homework)
admin.site.register(temp_homework)
