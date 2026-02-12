from django.db import models
from institutions.models import school
from datetime import datetime

# Create your models here.

class noticeboard(models.Model):
    title = models.CharField(max_length=100)
    notice_date = models.DateField(default=datetime.today)
    content = models.TextField()
    file = models.FileField(upload_to='notice_files/', blank=True, null=True)
    url = models.URLField(blank=True)
    status = models.CharField(max_length=10)
    notice_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class events(models.Model):
    event_title = models.CharField(max_length=100)
    event_desc= models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    post_date = models.DateField(blank=True,null=True)   
    event_location = models.CharField(max_length=200)
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    event_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.event_title
