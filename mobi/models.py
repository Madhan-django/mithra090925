from django.db import models
from institutions.models import school

# Create your models here.
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
