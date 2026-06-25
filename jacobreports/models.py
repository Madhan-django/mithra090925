from django.db import models


class ClassTeacherReport(models.Model):
    school_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)

    report_submitted_by = models.CharField(max_length=100)
    report_date = models.DateField()

    total_strength = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.branch} - {self.class_name} {self.section} ({self.report_date})"


class ClassStrength(models.Model):
    report = models.OneToOneField(
        ClassTeacherReport,
        on_delete=models.CASCADE,
        related_name="strength"
    )

    boys = models.PositiveIntegerField()
    girls = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"Strength: {self.total}"


class GeneralRemark(models.Model):
    REMARK_FOR_CHOICES = (
        ('parents', 'Parents'),
        ('pupils', 'Pupils'),
    )

    report = models.ForeignKey(
        ClassTeacherReport,
        on_delete=models.CASCADE,
        related_name="remarks"
    )

    remark_for = models.CharField(max_length=20, choices=REMARK_FOR_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f"{self.remark_for} remark"


class TransportDetail(models.Model):
    report = models.ForeignKey(
        ClassTeacherReport,
        on_delete=models.CASCADE,
        related_name="transport_details"
    )

    mode = models.CharField(max_length=100)  # Private Auto, Walk, Cycle etc.
    boys = models.PositiveIntegerField(default=0)
    girls = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total = self.boys + self.girls
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.mode} - {self.total}"


class TeacherMeeting(models.Model):
    report = models.OneToOneField(
        ClassTeacherReport,
        on_delete=models.CASCADE,
        related_name="meeting"
    )

    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Class Teacher Meeting"


class SuggestionGrievance(models.Model):
    report = models.OneToOneField(
        ClassTeacherReport,
        on_delete=models.CASCADE,
        related_name="suggestions"
    )

    details = models.TextField()

    def __str__(self):
        return "Suggestions & Grievances"
