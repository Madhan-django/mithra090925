from django.db import models
from institutions.models import school
from setup.models import sclass,currentacademicyr,academicyr,section
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


# Create your models here.
class enquiry(models.Model):
    enq_name = models.CharField(max_length=25)
    enq_student= models.CharField(max_length=25)
    enq_gender = models.CharField(max_length=15)
    enq_date = models.DateField()
    enq_followup = models.DateField()
    enq_class = models.ForeignKey(sclass, on_delete=models.CASCADE)
    enq_mob = models.CharField(max_length=10)
    enq_altmob = models.CharField(max_length=10,blank=True,null=True)
    enq_email = models.EmailField()
    enq_ref = models.CharField(max_length=25)
    enq_communication = models.CharField(max_length=25)
    enq_det = models.TextField()
    enq_status= models.CharField(max_length=10)
    school_name = models.ForeignKey(school,on_delete=models.CASCADE)
    acad_year = models.ForeignKey(currentacademicyr,on_delete=models.CASCADE)


    def __str__(self):
        return self.enq_name

class students(models.Model):
    first_name = models.CharField('First_Name', max_length=60)
    last_name = models.CharField('Last_name',max_length=60)
    gender = models.CharField(max_length=12,blank=True,null=True)
    dob_date = models.DateField()
    phone = models.CharField('phone', max_length=11)
    email = models.EmailField()
    address = models.CharField('address', max_length=250)
    admn_no = models.IntegerField()
    admn_date = models.DateField()
    religion = models.CharField('religion', max_length=15)
    caste = models.CharField('caste', max_length=50)
    blood_group = models.CharField('blood_group', max_length=3)
    father_name = models.CharField('fname', max_length=60)
    mother_name = models.CharField('mname', max_length=60)
    father_occupation = models.CharField('foccup', max_length=60)
    mother_occupation = models.CharField('moccup', max_length=60)
    student_photo = models.ImageField(upload_to='images/',null=True,blank=True)
    roll_no = models.CharField('rollno', max_length=6)
    ac_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    class_name = models.ForeignKey(sclass, on_delete=models.CASCADE)
    secs = models.ForeignKey(section,blank=True,null=True,on_delete=models.CASCADE)
    school_student = models.ForeignKey(school, on_delete=models.CASCADE)
    student_status = models.CharField(max_length=10)
    tc_date = models.DateField(null=True,blank=True)
    usernm = models.CharField(max_length=25,blank=True,null=True)

    def __str__(self):
        return self.first_name + self.last_name

