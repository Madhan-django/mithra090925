from django.db import models
from institutions.models import school
from admission.models import students
from setup.models import sclass,section,academicyr,currentacademicyr


# Create your models here.
class books(models.Model):
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    subject = models.CharField(max_length=80)
    price = models.FloatField()
    quantity = models.IntegerField()
    issued = models.IntegerField()
    desc = models.TextField()
    rack = models.CharField(max_length=50)
    book_no = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    book_school = models.ForeignKey(school,on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class book_issued(models.Model):
    book_title = models.ForeignKey(books,on_delete=models.CASCADE)
    issued_to = models.ForeignKey(students,on_delete=models.CASCADE)
    sclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    section = models.ForeignKey(section,on_delete=models.CASCADE)
    acd_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    issued_quantity = models.IntegerField(default=1)
    issued_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.book_title.title

class library_card(models.Model):
    card_no = models.CharField(max_length=10,unique=True)
    issued_to = models.ForeignKey(students,on_delete=models.CASCADE)
    acad_year = models.ForeignKey(currentacademicyr,on_delete=models.CASCADE)
    card_issued_date = models.DateField()
    lib_school = models.ForeignKey(school,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('issued_to', 'acad_year',)





