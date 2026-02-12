import datetime
import os
from django.db import models
from institutions.models import school
from admission.models import students
from setup.models import subjects,sclass,section,currentacademicyr
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class staff(models.Model):
    EmpCode = models.CharField(max_length=20, blank=True, null=True)
    BioCode = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    gender = models.CharField(max_length=12)
    dob = models.DateField()
    address= models.CharField(max_length=250)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    join = models.DateField()
    staff_photo = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.CharField(max_length=150)
    salary = models.FloatField()
    desg = models.CharField(max_length=150)
    qualification = models.CharField(max_length=150)
    status = models.CharField(max_length=10,default='Active')
    desc = models.CharField(max_length=150,blank=True,null=True)
    staff_school=models.ForeignKey(school,on_delete=models.CASCADE)
    certifications = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    subjects_taught = models.ManyToManyField(subjects, blank=True)
    permission_group = models.CharField(max_length=15)
    staff_user = models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class staff_attendance(models.Model):
    attndate = models.DateField()
    staff_name = models.CharField(max_length=50)
    status = models.CharField(max_length=13)
    staff_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.status

class staff_attendancegen(models.Model):
    attndate = models.DateField()
    staff_school = models.ForeignKey(school,on_delete=models.CASCADE)

    class Meta:
        unique_together = ['attndate', 'staff_school',]

class homework(models.Model):
    title = models.CharField(max_length=100)
    hclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    secs = models.ForeignKey(section,on_delete=models.CASCADE)
    subj = models.ForeignKey(subjects,on_delete=models.CASCADE)
    homework_date = models.DateField(default=datetime.datetime.today)
    attachment = models.FileField(upload_to='homework/', blank=True, null=True)
    description = models.CharField(max_length=155)
    submission_date = models.DateField(default=datetime.datetime.today)
    created_by = models.ForeignKey(staff, on_delete=models.CASCADE)
    acad_yr = models.ForeignKey(currentacademicyr, on_delete=models.CASCADE)
    school_homework = models.ForeignKey(school,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.title

def homework_upload_path(instance, filename):
    # Store file in media/homework/<year>/<filename>
    return os.path.join(
        "homework",
        str(instance.homework_date.year),
        filename
    )

class temp_homework(models.Model):
    title = models.CharField(max_length=100)
    hclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    secs = models.ForeignKey(section,on_delete=models.CASCADE)
    subj = models.ForeignKey(subjects,on_delete=models.CASCADE)
    homework_date = models.DateField(default=datetime.datetime.today)
    description = models.CharField(max_length=180)
    attachment = models.FileField(upload_to=homework_upload_path, blank=True, null=True)
    submission_date = models.DateField(default=datetime.datetime.today)
    created_by = models.ForeignKey(staff, on_delete=models.CASCADE)
    acad_yr = models.ForeignKey(currentacademicyr, on_delete=models.CASCADE)
    school_homework = models.ForeignKey(school,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.title







