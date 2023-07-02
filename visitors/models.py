from django.db import models
from institutions.models import school

# Create your models here.


class visitors(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    purpose = models.TextField()
    meeting_person = models.CharField(max_length=100)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='visitor_photos/', blank=True, null=True)
    visitors_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
