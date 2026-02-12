from django.db import models
from institutions.models import school

# Create your models here.
class Video(models.Model):
    VTitle = models.CharField(max_length=80)
    Vdesc = models.CharField(max_length=255)
    Vdate = models.DateField()
    Vpostdate = models.DateField()
    Vlink = models.CharField(max_length=255)
    VThumbnail = models.ImageField(upload_to='thumbnail/',null=True,blank=True)
    status = models.CharField(max_length=9)
    Vschool = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.VTitle
