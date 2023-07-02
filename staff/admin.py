from django.contrib import admin
from .models import staff,staff_attendance,homework

# Register your models here.
admin.site.register(staff)
admin.site.register(staff_attendance)
admin.site.register(homework)