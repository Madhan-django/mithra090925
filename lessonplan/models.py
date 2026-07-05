from django.db import models
from institutions.models import school
from setup.models import sclass, section, subjects, currentacademicyr
from staff.models import staff


TEACHING_METHODS = [
    ('Lecture', 'Lecture'),
    ('Discussion', 'Discussion'),
    ('Activity', 'Activity'),
    ('Demo', 'Demonstration'),
    ('Review', 'Review'),
    ('Assessment', 'Assessment'),
    ('Group Work', 'Group Work'),
]

PLAN_STATUS = [
    ('Planned', 'Planned'),
    ('Taught', 'Taught'),
    ('Skipped', 'Skipped'),
]


class LessonPlan(models.Model):
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    teacher = models.ForeignKey(staff, on_delete=models.CASCADE)
    subject = models.ForeignKey(subjects, on_delete=models.CASCADE)
    cls = models.ForeignKey(sclass, on_delete=models.CASCADE)
    section = models.ForeignKey(section, on_delete=models.CASCADE)
    acad_yr = models.ForeignKey(currentacademicyr, on_delete=models.CASCADE)

    date = models.DateField()
    period_number = models.PositiveSmallIntegerField(default=1)

    chapter = models.CharField(max_length=200)
    topic = models.CharField(max_length=300)
    objectives = models.TextField(blank=True)
    content_taught = models.TextField(blank=True)
    teaching_method = models.CharField(max_length=20, choices=TEACHING_METHODS, default='Lecture')
    status = models.CharField(max_length=10, choices=PLAN_STATUS, default='Planned')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-period_number']

    def __str__(self):
        return f"{self.cls} {self.section} | {self.subject} | {self.topic} ({self.date})"


class LessonPlanAssignment(models.Model):
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name='assignments')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()

    is_given = models.BooleanField(default=False)
    given_date = models.DateField(null=True, blank=True)

    is_corrected = models.BooleanField(default=False)
    corrected_date = models.DateField(null=True, blank=True)

    notify_sent = models.BooleanField(default=False)
    notified_at = models.DateTimeField(null=True, blank=True)
    notify_success_count = models.IntegerField(default=0)
    notify_total_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson_plan} – {self.title}"


class LessonPlanNote(models.Model):
    lesson_plan      = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name='notes')
    file_name        = models.CharField(max_length=255)
    mime_type        = models.CharField(max_length=100, blank=True)
    file_size_kb     = models.PositiveIntegerField(default=0)
    drive_file_id    = models.CharField(max_length=100)
    drive_view_url   = models.URLField(max_length=500)
    drive_download_url = models.URLField(max_length=500, blank=True)
    uploaded_at      = models.DateTimeField(auto_now_add=True)
    uploaded_by      = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.file_name
