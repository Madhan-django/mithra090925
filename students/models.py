from django.db import models
from setup.models import sclass,section


# Create your models here.

class attendance(models.Model):
    aclass= models.ForeignKey(sclass,on_delete=models.CASCADE)
    sec = models.ForeignKey(section,on_delete=models.CASCADE)
    attndate = models.DateField()
    student_name = models.CharField(max_length=50)
    status = models.CharField(max_length=13)

    def __str__(self):
        return self.status

class attendancegen(models.Model):
    aclass = models.ForeignKey(sclass, on_delete=models.CASCADE)
    sec = models.ForeignKey(section, on_delete=models.CASCADE)
    attndate = models.DateField()

    class Meta:
        unique_together = ('aclass', 'sec', 'attndate')


class attendanceview(models.Model):
    aclass = models.ForeignKey(sclass, on_delete=models.CASCADE)
    sec = models.ForeignKey(section, on_delete=models.CASCADE)
    attndate = models.DateField()