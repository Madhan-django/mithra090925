from django.db import models
from institutions.models import school
from django.contrib.auth.models import User

# Create your models here.
class fee_automate_report(models.Model):
    report_name = models.CharField(max_length=40)
    report_school = models.ForeignKey(school, on_delete=models.CASCADE)
    reporter_name = models.CharField(max_length=75)
    report_to = models.CharField(max_length=15)
    report_create_date= models.DateTimeField()
    report_status= models.CharField(max_length=10)

    def __str__(self):
        return self.report_name +" "+ self.report_to


class AutomateFunc(models.Model):
    SCHEDULE_TYPES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    TASKS = [
        ('fee_collection', 'Fee Collection'),
        ('petty_cash', 'Petty Cash'),
        ('stocks', 'Stocks'),
        ('summarys', 'Summary'),
        ('Grievance_Report','Grievance_Report'),
        ('Grievance_over_Due','Grievance_over_Due')
    ]

    SEND_TYPES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]

    creation_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=40, choices=TASKS)
    schedule_type = models.CharField(max_length=100, choices=SCHEDULE_TYPES)
    schedule_time = models.TimeField()
    automate_type = models.CharField(max_length=10, choices=SEND_TYPES)  # email or whatsapp
    send_to = models.CharField(max_length=100)  # email or mobile number
    school = models.ForeignKey(school, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-creation_date']
        verbose_name = "Automated Task"
        verbose_name_plural = "Automated Tasks"

    def __str__(self):
        return f"{self.task} - {self.schedule_type} at {self.schedule_time}"