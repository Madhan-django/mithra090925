from django.db import models
from institutions.models import school
from setup.models import sclass, section
from staff.models import staff


class ClassTeacherReport(models.Model):

    # =========================
    # BASIC DETAILS
    # =========================

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    class_name = models.ForeignKey(
        sclass,
        on_delete=models.CASCADE
    )

    section = models.ForeignKey(
        section,
        on_delete=models.CASCADE
    )

    report_submitted_by = models.ForeignKey(
        staff,
        on_delete=models.CASCADE
    )

    report_date = models.DateField()

    # =========================
    # GENERAL REPORT
    # =========================

    boys_on_roll = models.PositiveIntegerField(default=0)
    girls_on_roll = models.PositiveIntegerField(default=0)

    boys_present = models.PositiveIntegerField(default=0)
    girls_present = models.PositiveIntegerField(default=0)

    boys_uniform_defaulters = models.PositiveIntegerField(default=0)
    girls_uniform_defaulters = models.PositiveIntegerField(default=0)

    boys_absentees = models.PositiveIntegerField(default=0)
    girls_absentees = models.PositiveIntegerField(default=0)

    action_taken = models.TextField(
        blank=True,
        null=True
    )

    birthday_celebration = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # DAILY ROUTINE REPORT
    # =========================

    accident_details = models.TextField(
        blank=True,
        null=True
    )

    defaulters = models.TextField(
        blank=True,
        null=True
    )

    homework_details = models.TextField(
        blank=True,
        null=True
    )

    drill_work_details = models.TextField(
        blank=True,
        null=True
    )

    activity_class = models.TextField(
        blank=True,
        null=True
    )

    announcements = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # REMARKS
    # =========================

    teachers_remark = models.TextField(
        blank=True,
        null=True
    )

    parents_remark = models.TextField(
        blank=True,
        null=True
    )

    pupils_remark = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # TRANSPORT DETAILS
    # =========================

    private_auto_boys = models.PositiveIntegerField(default=0)
    private_auto_girls = models.PositiveIntegerField(default=0)

    cycle_boys = models.PositiveIntegerField(default=0)
    cycle_girls = models.PositiveIntegerField(default=0)

    walk_boys = models.PositiveIntegerField(default=0)
    walk_girls = models.PositiveIntegerField(default=0)

    school_van_boys = models.PositiveIntegerField(default=0)
    school_van_girls = models.PositiveIntegerField(default=0)

    bus_boys = models.PositiveIntegerField(default=0)
    bus_girls = models.PositiveIntegerField(default=0)

    others_boys = models.PositiveIntegerField(default=0)
    others_girls = models.PositiveIntegerField(default=0)

    # =========================
    # MEETING / SUGGESTIONS
    # =========================

    meeting_details = models.TextField(
        blank=True,
        null=True
    )

    suggestions_and_grievances = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # SYSTEM
    # =========================

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'class_name',
            'section',
            'report_date'
        )

    # =========================
    # CALCULATED TOTALS
    # =========================

    @property
    def total_on_roll(self):
        return self.boys_on_roll + self.girls_on_roll

    @property
    def total_present(self):
        return self.boys_present + self.girls_present

    @property
    def total_uniform_defaulters(self):
        return (
            self.boys_uniform_defaulters +
            self.girls_uniform_defaulters
        )

    @property
    def total_absentees(self):
        return self.boys_absentees + self.girls_absentees

    @property
    def private_auto_total(self):
        return (
            self.private_auto_boys +
            self.private_auto_girls
        )

    @property
    def cycle_total(self):
        return self.cycle_boys + self.cycle_girls

    @property
    def walk_total(self):
        return self.walk_boys + self.walk_girls

    @property
    def school_van_total(self):
        return (
            self.school_van_boys +
            self.school_van_girls
        )

    @property
    def bus_total(self):
        return self.bus_boys + self.bus_girls

    @property
    def others_total(self):
        return self.others_boys + self.others_girls

    @property
    def transport_grand_total(self):
        return (
            self.private_auto_total +
            self.cycle_total +
            self.walk_total +
            self.school_van_total +
            self.bus_total +
            self.others_total
        )

    def __str__(self):
        return (
            f"{self.class_name} "
            f"{self.section} - "
            f"{self.report_date}"
        )


class InchargeReport(models.Model):

    DEPARTMENT_CHOICES = [
        ('Primary', 'Primary'),
        ('Middle School', 'Middle School'),
        ('High School', 'High School'),
        ('Higher Secondary', 'Higher Secondary'),
    ]

    MORALS_CHOICES = [
        ('Given', 'Given'),
        ('Not Given', 'Not Given'),
    ]

    ATMOSPHERE_CHOICES = [
        ('Calm', 'Calm'),
        ('Noisy', 'Noisy'),
    ]

    NOISE_CHOICES = [
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low'),
    ]

    # =========================
    # BASIC DETAILS
    # =========================

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    report_submitted_by = models.ForeignKey(
        staff,
        on_delete=models.CASCADE
    )

    reporting_time = models.TimeField()

    report_date = models.DateField()

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    # =========================
    # MORNING SESSION
    # =========================

    late_comers_teachers = models.TextField(blank=True, null=True)

    late_comers_duty_teachers = models.TextField(blank=True, null=True)

    absentees_teachers = models.TextField(blank=True, null=True)

    zero_hour_maintained = models.BooleanField(default=False)

    assembly_arrangements = models.TextField(blank=True, null=True)

    class_teachers_morals = models.CharField(
        max_length=20,
        choices=MORALS_CHOICES,
        default='Given'
    )

    dispersing_time = models.TimeField(blank=True, null=True)

    # =========================
    # LUNCH BREAK
    # =========================

    ct_availability = models.BooleanField(default=True)

    children_without_lunch = models.PositiveIntegerField(default=0)

    lunch_atmosphere = models.CharField(
        max_length=10,
        choices=ATMOSPHERE_CHOICES,
        default='Calm'
    )

    noise_level = models.CharField(
        max_length=10,
        choices=NOISE_CHOICES,
        blank=True,
        null=True
    )

    # =========================
    # AFTERNOON SESSION
    # =========================

    cram_conducted = models.TextField(blank=True, null=True)

    special_class = models.TextField(blank=True, null=True)

    activity_class = models.TextField(blank=True, null=True)

    accident_details = models.TextField(blank=True, null=True)

    incidents = models.TextField(blank=True, null=True)

    pupils_detained = models.TextField(blank=True, null=True)

    # =========================
    # STATUS DETAILS
    # =========================

    class_work_given = models.BooleanField(default=False)

    homework_corrected = models.BooleanField(default=False)

    handbook_checked = models.BooleanField(default=False)

    supervising_report = models.TextField(blank=True, null=True)

    # =========================
    # PERIODS (MORNING)
    # =========================

    period_1 = models.TextField(blank=True, null=True)
    period_2 = models.TextField(blank=True, null=True)
    period_3 = models.TextField(blank=True, null=True)
    period_4 = models.TextField(blank=True, null=True)

    # =========================
    # PERIODS (NOON)
    # =========================

    period_5 = models.TextField(blank=True, null=True)
    period_6 = models.TextField(blank=True, null=True)
    period_7 = models.TextField(blank=True, null=True)
    period_8 = models.TextField(blank=True, null=True)

    # =========================
    # CIRCULAR DETAILS
    # =========================

    circular_teachers = models.TextField(blank=True, null=True)
    circular_parents = models.TextField(blank=True, null=True)
    circular_pupils = models.TextField(blank=True, null=True)

    # =========================
    # OCCURRENCES
    # =========================

    birthday = models.TextField(blank=True, null=True)
    competition_field_trip = models.TextField(blank=True, null=True)
    celebration = models.TextField(blank=True, null=True)
    meeting_conducted = models.TextField(blank=True, null=True)
    meeting_details = models.TextField(blank=True, null=True)
    demo_class = models.TextField(blank=True, null=True)

    # =========================
    # ROUNDS REPORT
    # =========================

    rounds_report = models.TextField(blank=True, null=True)

    # =========================
    # STAFF PRAYER
    # =========================

    staff_prayer_attendance = models.TextField(blank=True, null=True)

    # =========================
    # SUGGESTIONS
    # =========================

    suggestions_and_grievances = models.TextField(blank=True, null=True)

    # =========================
    # LATE EVENING CLASS
    # =========================

    late_evening_class_std = models.CharField(max_length=50, blank=True, null=True)
    late_evening_class_subject = models.CharField(max_length=100, blank=True, null=True)
    late_evening_class_teacher = models.CharField(max_length=100, blank=True, null=True)
    late_evening_class_students = models.PositiveIntegerField(default=0)

    # =========================
    # TOMORROW'S ASSIGNMENT
    # =========================

    tomorrows_assignment = models.TextField(blank=True, null=True)

    # =========================
    # SYSTEM
    # =========================

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school_name', 'department', 'report_date')
        ordering = ['-report_date', '-id']

    def __str__(self):
        return (
            f"{self.department} - "
            f"{self.report_submitted_by} - "
            f"{self.report_date}"
        )