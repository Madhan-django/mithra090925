from django.db import models
from institutions.models import school
from admission.models import students
from staff.models import staff
from setup.models import sclass,section


# Create your models here.
class GeneralNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    post_date = models.DateTimeField()
    post_to = models.ManyToManyField(students, related_name='notifications_received')
    created_by_id = models.ForeignKey(staff,on_delete=models.CASCADE, related_name='created_notifications')
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=12)
    Notification_school = models.ForeignKey(school, on_delete=models.CASCADE, related_name='Notification_school')
    success_count = models.IntegerField(default=0,null=True,blank=True)
    total_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title
        
class temp_GeneralNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    post_date = models.DateTimeField()
    post_to = models.ManyToManyField(students)
    created_by_id = models.ForeignKey(staff,on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    status = models.CharField(max_length=12)
    Notification_school = models.ForeignKey(school, on_delete=models.CASCADE)
    success_count = models.IntegerField(default=0,null=True,blank=True)
    total_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title
        
        
class SectionwiseNotification(models.Model):
    title_msg = models.CharField(max_length=50)
    message_cont = models.CharField(max_length=155)
    aclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    ssec = models.ForeignKey(section,on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    post_date = models.DateTimeField()
    created_by = models.ForeignKey(staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=12)
    Notification_school = models.ForeignKey(school, on_delete=models.CASCADE)
    success_count = models.IntegerField(default=0, null=True, blank=True)
    total_count = models.IntegerField(default=0, null=True, blank=True)

class SchoolNotification(models.Model):
    title_msg = models.CharField(max_length=50)
    message_cont = models.CharField(max_length=155)
    create_date = models.DateTimeField()
    post_date = models.DateTimeField()
    created_by = models.ForeignKey(staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=12)
    Notification_school = models.ForeignKey(school, on_delete=models.CASCADE)
    success_count = models.IntegerField(default=0, null=True, blank=True)
    total_count = models.IntegerField(default=0, null=True, blank=True)

class StaffNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    post_to = models.ManyToManyField(staff, through='StaffNotificationRecipient')
    created_by_id = models.ForeignKey(staff, on_delete=models.CASCADE, related_name='created_staff_notifications')
    status = models.CharField(max_length=12)
    Notification_school = models.ForeignKey(school, on_delete=models.CASCADE, related_name='staff_notification_school')
    success_count = models.IntegerField(default=0, null=True, blank=True)
    total_count = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title


class StaffNotificationRecipient(models.Model):
    notification = models.ForeignKey(StaffNotification, on_delete=models.CASCADE, related_name='recipients')
    staff = models.ForeignKey(staff, on_delete=models.CASCADE, related_name='notification_receipts')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('notification', 'staff')

    def __str__(self):
        return f"{self.notification.title} -> {self.staff}"