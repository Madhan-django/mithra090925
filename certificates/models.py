import datetime
from django.db import models
from django.contrib.auth.models import User
from institutions.models import school
from admission.models import students

CERT_TYPES = [
    ('TC',        'Transfer Certificate'),
    ('BONAFIDE',  'Bonafide Certificate'),
    ('CHARACTER', 'Character Certificate'),
    ('STUDY',     'Study Certificate'),
    ('SPORTS',    'Sports Certificate'),
    ('CUSTOM',    'Custom Certificate'),
]


class CertificateTemplate(models.Model):
    school        = models.ForeignKey(school, on_delete=models.CASCADE, related_name='cert_templates')
    name          = models.CharField(max_length=100)
    cert_type     = models.CharField(max_length=20, choices=CERT_TYPES, default='CUSTOM')
    template_file = models.FileField(upload_to='cert_templates/')
    is_active     = models.BooleanField(default=True)
    notes         = models.TextField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['cert_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_cert_type_display()}) — {self.school.name}"


class CertificateIssued(models.Model):
    school        = models.ForeignKey(school, on_delete=models.CASCADE)
    student       = models.ForeignKey(students, on_delete=models.CASCADE)
    template      = models.ForeignKey(CertificateTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    cert_number   = models.CharField(max_length=30, unique=True)
    cert_type     = models.CharField(max_length=20, choices=CERT_TYPES)
    issued_date   = models.DateField(default=datetime.date.today)
    issued_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    extra_context = models.JSONField(default=dict, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_date', '-created_at']

    def __str__(self):
        return f"{self.cert_number} — {self.student}"
