from django.db import models
from setup.models import academicyr
from institutions.models import school
from setup.models import academicyr,sclass,subjects
from admission.models import students

# Create your models here.

class exam_group(models.Model):
    exm_group = models.CharField(max_length=15)
    exam_group_school = models.ForeignKey(school,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.exm_group




class exams(models.Model):
    exam_title = models.CharField(max_length=50)
    exam_code = models.CharField(max_length=50)
    exam_centre = models.CharField(max_length=50)
    exam_class = models.ForeignKey(sclass,on_delete=models.CASCADE)
    exam_Sub_count= models.IntegerField()
    exam_groupby = models.CharField(max_length=25,blank=True,null=True)
    exm_grp = models.ForeignKey(exam_group, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    exam_start_date = models.DateField()
    exam_end_date = models.DateField()
    exam_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    exam_school = models.ForeignKey(school,on_delete=models.CASCADE)
    published = models.CharField(max_length=6,blank=True,null=True)
    remark = models.CharField(max_length=6)

    def __str__(self):
       return self.exam_title

class exam_subjectmap(models.Model):
    exname= models.ForeignKey(exams,on_delete=models.CASCADE)
    exam_subjects = models.ForeignKey(subjects,on_delete=models.CASCADE)
    exam_subject_type = models.CharField(max_length=15)
    paper_code = models.CharField(max_length=10)
    paper_date = models.DateField()
    start_time= models.TimeField()
    end_time= models.TimeField()
    room_no = models.CharField(max_length=10)
    max_marks = models.IntegerField()


    def __str__(self):
        return self.exam_subjects.subject_name



class admit_card(models.Model):
    examno = models.CharField(max_length=10)
    exam_stu = models.ForeignKey(students,on_delete=models.CASCADE)
    exam_label = models.ForeignKey(exams,on_delete=models.CASCADE)

    def __str__(self):
        return self.examno

class temp_insert(models.Model):
    exam_prefix = models.CharField(max_length=5)
    exam_start_no = models.IntegerField()


    def __str__(self):
        return self.exam_prefix

class exam_result(models.Model):
    obtained_marks = models.IntegerField(blank=True,null=True)
    exam_sub = models.ForeignKey(exam_subjectmap,on_delete=models.CASCADE)
    adm_card = models.ForeignKey(admit_card,on_delete=models.CASCADE)
    remark = models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.adm_card.exam_stu.first_name

