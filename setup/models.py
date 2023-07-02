from django.db import models
from institutions.models import school


# Create your models here.

class academicyr(models.Model):
    acad_year = models.CharField(max_length=10)
    school_name = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.acad_year


class currentacademicyr(models.Model):
    school_name = models.ForeignKey(school,on_delete=models.CASCADE)
    current_year = models.ForeignKey(academicyr,on_delete=models.PROTECT)

    def __str__(self):
        return self.current_year.acad_year



class sclass(models.Model):
    name = models.CharField(max_length=50)
    acad_year = models.ForeignKey(currentacademicyr,on_delete=models.CASCADE)
    school_name=models.ForeignKey(school,on_delete=models.CASCADE,related_name='school_nam')

    class Meta:
        unique_together = ('name', 'acad_year',)
    def  __str__(self):
        return self.name

class section(models.Model):
    section_name = models.CharField(max_length=50)
    acad_year = models.ForeignKey(currentacademicyr, on_delete=models.CASCADE)
    school_name = models.ForeignKey(school, on_delete=models.CASCADE, related_name='sec_school_name')
    class_sec_name= models.ForeignKey(sclass,on_delete=models.CASCADE)




    def __str__(self):
        return self.section_name


class subjects(models.Model):
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=10)
    subject_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    subject_class = models.ForeignKey(sclass,on_delete=models.CASCADE)
    subject_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name

