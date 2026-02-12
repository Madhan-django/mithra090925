from django.db import models
from institutions.models import school
from setup.models import sclass,section,academicyr
from admission.models import students


class Grievance(models.Model):

    # Foreign Keys
    gschool = models.ForeignKey(school, on_delete=models.CASCADE)
    gclass = models.ForeignKey(sclass,on_delete=models.SET_NULL,blank=True,null=True)
    gsec = models.ForeignKey(section, on_delete=models.SET_NULL, null=True, blank=True)
    stud_name = models.ForeignKey(students, on_delete=models.SET_NULL, null=True, blank=True)
    ac_year = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    # Other Fields
    mobile = models.CharField('phone', max_length=11)

    AREA_CHOICES = [
        ('Academic', 'Academic'),
        ('Non-Academic', 'Non-Academic'),
        ('Activities', 'Activities'),
        ('Transport', 'Transport'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    ]
    area_of_complaint = models.CharField(max_length=20, choices=AREA_CHOICES)

    aoc_other = models.CharField(max_length=50, null=True, blank=True)

    detail = models.TextField(max_length=250)

    principal_remark = models.CharField(max_length=100, null=True, blank=True)
    concern_person_remark = models.CharField(max_length=100, null=True, blank=True)
    act_details = models.CharField(max_length=100, null=True, blank=True)

    INTIMATION_CHOICES = [
        ('Oral', 'Oral'),
        ('Phone', 'Phone'),
        ('In-Person', 'In-Person'),
        ('Email', 'Email'),
        ('Whatsapp', 'Whatsapp'),
        ('APP', 'APP'),
    ]
    act_intimation_to_person = models.CharField(max_length=20, choices=INTIMATION_CHOICES)

    complaint_date = models.DateTimeField()
    action_date = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Pending', 'Pending'),
        ('In-progress', 'In-progress'),
        ('Resolved', 'Resolved'),
    ]
    complaint_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    complaint_received = models.CharField(max_length=20, choices=INTIMATION_CHOICES)

    concern_person_name = models.CharField(max_length=150, default="Anonymous")
    no_action_taken = models.BooleanField(default=True)
    def __str__(self):
        return f"Complaint by {self.stud_name} - {self.area_of_complaint}"
