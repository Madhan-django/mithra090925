from django.db import models
from institutions.models import school

# Create your models here.
class Banner(models.Model):
    school_name   = models.ForeignKey(school, on_delete=models.CASCADE, related_name='banners')
    title         = models.CharField(max_length=200)
    image         = models.ImageField(upload_to='school/banners/')
    link_url      = models.URLField(blank=True)
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    start_date    = models.DateField(blank=True, null=True)
    end_date      = models.DateField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.school_name} — {self.title}"


class DeviceFCMToken(models.Model):
    firecmToken = models.CharField(max_length=255)
    username = models.CharField(max_length=15)

    def __str__(self):
        return self.firecmToken



class SchoolProfile(models.Model):
    school_name     = models.ForeignKey(school,on_delete=models.CASCADE)
    tagline         = models.CharField(max_length=200, blank=True)
    about           = models.TextField()
    logo            = models.ImageField(upload_to='school/logo/')
    founder_name    = models.CharField(max_length=200)
    founder_pic     = models.ImageField(upload_to='school/founder/', blank=True, null=True)
    founded_year    = models.CharField(max_length=10)
    city            = models.CharField(max_length=100)
    phone           = models.CharField(max_length=20)
    email           = models.EmailField()
    address         = models.TextField()
    admission_open  = models.BooleanField(default=False)
    admission_url   = models.URLField(blank=True)   # ← add
    gallery_url     = models.URLField(blank=True)   # ← add



class GalleryPhoto(models.Model):
    title         = models.CharField(max_length=200)
    album         = models.CharField(max_length=100, blank=True, help_text='e.g. Annual Day, Sports Meet')
    drive_file_id = models.CharField(max_length=200, blank=True, default='')
    view_url      = models.URLField(blank=True)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    school        = models.ForeignKey(school, on_delete=models.CASCADE, related_name='gallery_photos')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PhotoGallery(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    PTitle     = models.CharField(max_length=255)
    PThumbnail = models.URLField(blank=True)
    Plink      = models.URLField(blank=True)
    Pdesc      = models.TextField(blank=True)
    Pdate      = models.DateField(null=True, blank=True)
    Ppostdate  = models.DateField(auto_now_add=True)
    Pschool    = models.ForeignKey(school, on_delete=models.CASCADE, related_name='photo_gallery')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        ordering = ["-Ppostdate"]

    def __str__(self):
        return self.PTitle


class VideoGallery(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    VTitle     = models.CharField(max_length=255)
    VThumbnail = models.URLField(blank=True)
    Vlink      = models.URLField(blank=True)
    Vdesc      = models.TextField(blank=True)
    Vdate      = models.DateField(null=True, blank=True)
    Vpostdate  = models.DateField(auto_now_add=True)
    Vschool    = models.ForeignKey(school, on_delete=models.CASCADE, related_name='video_gallery')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        ordering = ["-Vpostdate"]

    def __str__(self):
        return self.VTitle
