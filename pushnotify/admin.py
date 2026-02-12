from django.contrib import admin
from .models import GeneralNotification,temp_GeneralNotification,SectionwiseNotification,SchoolNotification

# Register your models here.
admin.site.register(GeneralNotification)
admin.site.register(temp_GeneralNotification)
admin.site.register(SectionwiseNotification)
admin.site.register(SchoolNotification)