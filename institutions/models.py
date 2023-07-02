from django.db import models

# Create your models here.
class school(models.Model):
    name = models.CharField('school', max_length=50)
    phone = models.CharField('phone', max_length=11)
    email = models.EmailField()
    address = models.TextField('address', max_length=150)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    regno = models.CharField('regno', max_length=50)
    isactive=models.BooleanField()

    def __str__(self):
        return self.name