# timetable/models.py
from django.db import models
from staff.models import staff
from setup.models import subjects, section, sclass
from institutions.models import school

class Teacher(models.Model):
    name = models.ForeignKey(staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name.first_name} {self.name.last_name}"

class TimeSlot(models.Model):
    DAYS = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    ]
    day = models.CharField(max_length=3, choices=DAYS)
    period_number = models.IntegerField()  # 1, 2, 3... up to max periods per day
    period_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_day_display()} - Period {self.period_number}"

class TeachingAllocation(models.Model):
    teacher = models.ForeignKey(staff, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    section = models.ForeignKey(section, on_delete=models.CASCADE)  # section includes class
    hours_per_week = models.IntegerField()
    teacher_school = models.ForeignKey(school, on_delete=models.CASCADE)
    not_first = models.BooleanField(default=False)
    not_last = models.BooleanField(default=False)
    is_classteacher = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.section.class_sec_name.name} - {self.section.section_name} | {self.subject.subject_name} by {self.teacher} - {self.hours_per_week} hrs"

class Timetable(models.Model):
    section = models.ForeignKey(section, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(staff, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    timetable_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.section.class_sec_name.name}-{self.section.section_name} | {self.subject.subject_name} - {self.teacher} @ {self.timeslot}"

class ReservedSlot(models.Model):
    sch_class= models.ForeignKey(sclass,on_delete=models.CASCADE)
    section = models.ForeignKey(section, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    adaptive_day= models.BooleanField(default=False,blank=True,null=True)
    adaptive_period = models.BooleanField(default=False, blank=True, null=True)
    school = models.ForeignKey(school, on_delete=models.CASCADE)