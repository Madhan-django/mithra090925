from django.db import models

# Create your models here.
class school(models.Model):
    name = models.CharField('school', max_length=50)
    phone = models.CharField('phone', max_length=11)
    email = models.EmailField()
    website = models.CharField(max_length=80,blank=True,null=True)
    address = models.TextField('address', max_length=150)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    notification_logo= models.ImageField(upload_to='logos/',blank=True,null=True)
    regno = models.CharField('regno', max_length=50)
    isactive=models.BooleanField()
    web_aboutus = models.CharField(max_length=80,blank=True,null=True)
    web_contactus = models.CharField(max_length=80,blank=True,null=True)
    web_gallery = models.CharField(max_length=80,blank=True,null=True)
    web_admission = models.CharField(max_length=80,blank=True,null=True)

    def __str__(self):
        return self.name