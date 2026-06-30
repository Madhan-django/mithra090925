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