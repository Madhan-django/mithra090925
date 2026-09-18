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
    def attendance_pct(self):
        total = self.total_on_roll
        if not total:
            return 0
        return round((self.total_present / total) * 100, 1)

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


class ClassTeacherMapping(models.Model):
    """Maps an incharge staff to the class teachers they supervise."""

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    incharge = models.ForeignKey(
        staff,
        on_delete=models.CASCADE,
        related_name='supervised_teachers'
    )

    class_teacher = models.ForeignKey(
        staff,
        on_delete=models.CASCADE,
        related_name='incharge_mappings'
    )

    class Meta:
        unique_together = ('incharge', 'class_teacher')

    def __str__(self):
        return (
            f"{self.incharge} → {self.class_teacher}"
        )


class InchargeMapping(models.Model):
    """Maps a supervisor to the incharges they oversee."""

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    supervisor = models.ForeignKey(
        staff,
        on_delete=models.CASCADE,
        related_name='supervised_incharges'
    )

    incharge = models.ForeignKey(
        staff,
        on_delete=models.CASCADE,
        related_name='supervisor_mappings'
    )

    class Meta:
        unique_together = ('supervisor', 'incharge')

    def __str__(self):
        return f"{self.supervisor} → {self.incharge}"


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

    STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Open', 'Open'),
        ('In-Progress', 'In-Progress'),
        ('Issue', 'Issue'),
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

    late_comers_pupils = models.TextField(blank=True, null=True)

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
    # MORNING SPECIAL CLASS
    # =========================

    morning_spl_class_schedule = models.TextField(blank=True, null=True)

    morning_spl_late_comers = models.TextField(blank=True, null=True)

    duty_alteration = models.TextField(blank=True, null=True)

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

    breakfast_count = models.PositiveIntegerField(default=0)

    children_permission = models.TextField(blank=True, null=True)

    pet_class_details = models.TextField(blank=True, null=True)

    parent_intimation = models.TextField(blank=True, null=True)

    # =========================
    # AFTERNOON SESSION
    # =========================

    cram_conducted = models.TextField(blank=True, null=True)

    cram_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    special_class = models.TextField(blank=True, null=True)

    activity_class = models.TextField(blank=True, null=True)

    accident_details = models.TextField(blank=True, null=True)

    incidents = models.TextField(blank=True, null=True)

    incident_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    pupils_detained = models.TextField(blank=True, null=True)

    # =========================
    # STATUS DETAILS
    # =========================

    class_work_given = models.BooleanField(default=False)

    homework_corrected = models.BooleanField(default=False)

    handbook_checked = models.BooleanField(default=False)

    handbook_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    homework_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

    supervising_report = models.TextField(blank=True, null=True)

    # =========================
    # PERIODS (MORNING)
    # =========================

    period_1_time = models.CharField(max_length=20, blank=True, null=True)
    period_1 = models.TextField(blank=True, null=True)

    period_2_time = models.CharField(max_length=20, blank=True, null=True)
    period_2 = models.TextField(blank=True, null=True)

    period_3_time = models.CharField(max_length=20, blank=True, null=True)
    period_3 = models.TextField(blank=True, null=True)

    period_4_time = models.CharField(max_length=20, blank=True, null=True)
    period_4 = models.TextField(blank=True, null=True)

    # =========================
    # PERIODS (NOON)
    # =========================

    period_5_time = models.CharField(max_length=20, blank=True, null=True)
    period_5 = models.TextField(blank=True, null=True)

    period_6_time = models.CharField(max_length=20, blank=True, null=True)
    period_6 = models.TextField(blank=True, null=True)

    period_7_time = models.CharField(max_length=20, blank=True, null=True)
    period_7 = models.TextField(blank=True, null=True)

    period_8_time = models.CharField(max_length=20, blank=True, null=True)
    period_8 = models.TextField(blank=True, null=True)

    # =========================
    # CIRCULAR DETAILS
    # =========================

    circular_teachers = models.TextField(blank=True, null=True)
    circular_parents = models.TextField(blank=True, null=True)
    circular_pupils = models.TextField(blank=True, null=True)
    circular_school = models.TextField(blank=True, null=True)

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

    late_evening_class = models.TextField(blank=True, null=True)

    # =========================
    # NOTE
    # =========================

    note = models.TextField(blank=True, null=True)

    note_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)

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


class PrincipalLogEntryType(models.Model):
    """Configurable entry types for the Principal's Daily Log."""

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=60)

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('school_name', 'name')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    # Default types seeded per school on first use
    DEFAULT_TYPES = [
        "Today's Schedule",
        "Observations & Complaints",
        "Suggestions & Grievances",
        "Activities",
        "Follow Up",
        "Meeting Agenda",
        "Incidents & Accidents",
        "Resolution",
    ]

    @classmethod
    def seed_defaults(cls, school_obj):
        for i, name in enumerate(cls.DEFAULT_TYPES):
            cls.objects.get_or_create(school_name=school_obj, name=name, defaults={'order': i})


class PrincipalDailyLog(models.Model):

    STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Open', 'Open'),
        ('In-Progress', 'In-Progress'),
        ('Issue', 'Issue'),
    ]

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    entry_date = models.DateField()

    entry_type = models.CharField(max_length=60)

    description = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='Closed'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_date', 'entry_type', 'id']

    def __str__(self):
        return f"{self.entry_date} | {self.entry_type}"


class MorningReport(models.Model):

    STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Open', 'Open'),
        ('In-Progress', 'In-Progress'),
        ('Issue', 'Issue'),
    ]

    school_name = models.ForeignKey(school, on_delete=models.CASCADE)
    report_date = models.DateField()
    report_submitted_by = models.ForeignKey(staff, on_delete=models.CASCADE)
    overall_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Closed')

    # Incharges Reporting Time
    senior_vp_time = models.CharField(max_length=10, blank=True, null=True)
    hr_sec_vp_time = models.CharField(max_length=10, blank=True, null=True)
    high_school_vp_time = models.CharField(max_length=10, blank=True, null=True)
    primary_vp_time = models.CharField(max_length=10, blank=True, null=True)
    office_incharge1_time = models.CharField(max_length=10, blank=True, null=True)
    office_incharge2_time = models.CharField(max_length=10, blank=True, null=True)
    maintenance_incharge_time = models.CharField(max_length=10, blank=True, null=True)

    # Morning Duty Teachers
    morning_duty_attended = models.CharField(max_length=20, blank=True, null=True)
    morning_duty_not_attended = models.CharField(max_length=20, blank=True, null=True)

    # Office
    office_opened_time = models.CharField(max_length=10, blank=True, null=True)
    parent_complaints = models.TextField(blank=True, null=True)

    # Teaching Staff
    teachers_present = models.PositiveIntegerField(default=0)
    teachers_absent = models.PositiveIntegerField(default=0)
    absentees_teachers = models.TextField(blank=True, null=True)
    absentees_non_teaching = models.TextField(blank=True, null=True)
    late_comers_teachers = models.TextField(blank=True, null=True)
    late_comers_spl_duty = models.TextField(blank=True, null=True)

    # Late Comers (Pupils)
    late_pupils_primary = models.CharField(max_length=20, blank=True, null=True)
    late_pupils_high_school = models.CharField(max_length=20, blank=True, null=True)
    late_pupils_hr_sec = models.CharField(max_length=20, blank=True, null=True)
    late_pupils_total = models.CharField(max_length=20, blank=True, null=True)

    # General
    general_instruction_by = models.TextField(blank=True, null=True)
    zero_hour_maintained = models.BooleanField(default=False)
    assembly_arrangement = models.TextField(blank=True, null=True)
    birthday_celebration = models.TextField(blank=True, null=True)

    # Roll Call
    rollcall_primary_present = models.PositiveIntegerField(default=0)
    rollcall_primary_total = models.PositiveIntegerField(default=0)
    rollcall_primary_absent = models.PositiveIntegerField(default=0)
    rollcall_high_school_present = models.PositiveIntegerField(default=0)
    rollcall_high_school_total = models.PositiveIntegerField(default=0)
    rollcall_high_school_absent = models.PositiveIntegerField(default=0)
    rollcall_hr_sec_present = models.PositiveIntegerField(default=0)
    rollcall_hr_sec_total = models.PositiveIntegerField(default=0)
    rollcall_hr_sec_absent = models.PositiveIntegerField(default=0)

    # Defaulters
    defaulters_uniform = models.CharField(max_length=20, blank=True, null=True)
    defaulters_haircut = models.CharField(max_length=20, blank=True, null=True)
    defaulters_nailcut = models.CharField(max_length=20, blank=True, null=True)
    defaulters_shoes = models.CharField(max_length=20, blank=True, null=True)
    defaulters_socks = models.CharField(max_length=20, blank=True, null=True)
    defaulters_tie = models.CharField(max_length=20, blank=True, null=True)
    defaulters_belt = models.CharField(max_length=20, blank=True, null=True)
    defaulters_id_card = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school_name', 'report_date')
        ordering = ['-report_date']

    def __str__(self):
        return f"Morning Report - {self.report_date}"

    @property
    def rollcall_total_present(self):
        return (
            self.rollcall_primary_present +
            self.rollcall_high_school_present +
            self.rollcall_hr_sec_present
        )

    @property
    def rollcall_total_strength(self):
        return (
            self.rollcall_primary_total +
            self.rollcall_high_school_total +
            self.rollcall_hr_sec_total
        )

    @property
    def rollcall_total_absent(self):
        return (
            self.rollcall_primary_absent +
            self.rollcall_high_school_absent +
            self.rollcall_hr_sec_absent
        )


class MorningReportSubstaff(models.Model):

    STATUS_CHOICES = [
        ('Closed', 'Closed'),
        ('Open', 'Open'),
        ('In-Progress', 'In-Progress'),
        ('Issue', 'Issue'),
    ]

    report = models.ForeignKey(
        MorningReport,
        on_delete=models.CASCADE,
        related_name='substaffs'
    )
    name = models.CharField(max_length=100)
    reporting_time = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Closed')

    def __str__(self):
        return f"{self.name} - {self.reporting_time}"


class PrincipalLogAccessMapping(models.Model):
    """Staff members permitted to do CRUD on PrincipalDailyLog (beyond admin/superadmin)."""

    school_name = models.ForeignKey(
        school,
        on_delete=models.CASCADE
    )

    staff_member = models.ForeignKey(
        staff,
        on_delete=models.CASCADE,
        related_name='principal_log_access'
    )

    class Meta:
        unique_together = ('school_name', 'staff_member')

    def __str__(self):
        return f"{self.school_name} → {self.staff_member}"