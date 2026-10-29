from django.contrib import admin
from .models import DeviceFCMToken, Banner, PhotoGallery, VideoGallery

@admin.register(DeviceFCMToken)
class DeviceFCMTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "firecmToken")   # columns shown in admin list
    search_fields = ("username", "firecmToken")        # enables search


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "school_name", "title", "is_active", "display_order", "start_date", "end_date")
    list_filter  = ("is_active", "school_name")
    search_fields = ("title",)



@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display  = ("id", "Pschool", "PTitle", "status", "Pdate", "Ppostdate")
    list_filter   = ("status", "Pschool")
    search_fields = ("PTitle",)


@admin.register(VideoGallery)
class VideoGalleryAdmin(admin.ModelAdmin):
    list_display  = ("id", "Vschool", "VTitle", "status", "Vdate", "Vpostdate")
    list_filter   = ("status", "Vschool")
    search_fields = ("VTitle",)
