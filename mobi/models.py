from django.db import models

# Create your models here.
class DeviceFCMToken(models.Model):
    firecmToken = models.CharField(max_length=255)
    username = models.CharField(max_length=15)

    def __str__(self):
        return self.firecmToken
