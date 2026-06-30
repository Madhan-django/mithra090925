from django.contrib import admin
from .models import academicyr,currentacademicyr,sclass,receipt_template

# Register your models here.
admin.site.register(academicyr)
admin.site.register(currentacademicyr)
admin.site.register(sclass)
admin.site.register(receipt_template)
