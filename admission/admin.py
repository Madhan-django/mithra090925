from django.contrib import admin
from .models import enquiry,students

class StudentsAdmin(admin.ModelAdmin):
    search_fields = ['id', 'first_name', 'email', 'phone']
    list_display = ('id', 'first_name', 'email', 'phone')# Add fields for search

admin.site.register(enquiry)
admin.site.register(students, StudentsAdmin)
