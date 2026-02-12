from django.contrib import admin
from .models import DeviceFCMToken

@admin.register(DeviceFCMToken)
class DeviceFCMTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "firecmToken")   # columns shown in admin list
    search_fields = ("username", "firecmToken")        # enables search
