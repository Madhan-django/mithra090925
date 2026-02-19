from django.contrib import admin
from .models import Department,Designation,Attendance

# Register your models here.

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Attendance)