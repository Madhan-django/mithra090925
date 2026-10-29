from django.db import models
from django.contrib.auth.models import User
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
        
        
class homework_time(models.Model):
    time = models.TimeField()
    homework_school = models.ForeignKey(school,on_delete=models.CASCADE)
    
    def __str__(slf):
        return self.time


class birthday_wish_config(models.Model):
    school = models.OneToOneField(school, on_delete=models.CASCADE, related_name='birthday_wish_config')
    title = models.CharField(
        max_length=200,
        default='Happy Birthday, {{student_name}}!',
        help_text='Use {{student_name}} to include the student name in the heading.'
    )
    message = models.TextField(
        default='Wishing {{student_name}} a very Happy Birthday! 🎂',
        help_text='Use {{student_name}} to personalize the message.'
    )
    time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Birthday Wish Config - {self.school}"


class subjects(models.Model):
    subject_name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=10)
    subject_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    subject_class = models.ForeignKey(sclass,on_delete=models.CASCADE)
    subject_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name

class receipt_template(models.Model):
    template = models.CharField(max_length=50)
    school_name = models.ForeignKey(school, on_delete=models.CASCADE)


    def __str__(self):
        return self.template


class AppUpdate(models.Model):
    BADGE_CHOICES = [
        ('New', 'New'),
        ('Improved', 'Improved'),
        ('Fixed', 'Fixed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='New')
    icon = models.CharField(max_length=60, default='ri-star-line',
                            help_text='Remix icon class, e.g. ri-star-line')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class StaffAnnouncement(models.Model):
    school      = models.ForeignKey(school, on_delete=models.CASCADE, related_name='staff_announcements')
    title       = models.CharField(max_length=200)
    body        = models.TextField()
    posted_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_on  = models.DateField(null=True, blank=True, help_text='Leave blank to never expire')
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title