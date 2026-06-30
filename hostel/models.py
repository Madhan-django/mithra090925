from django.db import models
from django.contrib.auth.models import User
from institutions.models import school
from admission.models import students
from setup.models import academicyr


# ─── Choices ──────────────────────────────────────────────────────────────────

HOSTEL_TYPE = [
    ('Boys',   'Boys'),
    ('Girls',  'Girls'),
    ('Co-ed',  'Co-ed'),
    ('Staff',  'Staff'),
]

HOSTEL_STATUS = [
    ('Active',   'Active'),
    ('Inactive', 'Inactive'),
]

ROOM_TYPE = [
    ('Single',    'Single'),
    ('Double',    'Double'),
    ('Triple',    'Triple'),
    ('Dormitory', 'Dormitory'),
    ('AC',        'AC Room'),
    ('Non-AC',    'Non-AC Room'),
]

ROOM_STATUS = [
    ('Available',   'Available'),
    ('Full',        'Full'),
    ('Maintenance', 'Under Maintenance'),
]

BED_STATUS = [
    ('Available',   'Available'),
    ('Occupied',    'Occupied'),
    ('Maintenance', 'Maintenance'),
]

FEE_PERIOD = [
    ('One-time',   'One-time'),
    ('Monthly',    'Monthly'),
    ('Quarterly',  'Quarterly'),
    ('Half-Yearly','Half-Yearly'),
    ('Annual',     'Annual'),
]

PAYMENT_MODE = [
    ('Cash',   'Cash'),
    ('Online', 'Online'),
    ('Cheque', 'Cheque'),
    ('DD',     'Demand Draft'),
    ('UPI',    'UPI'),
]

INVOICE_STATUS = [
    ('Pending', 'Pending'),
    ('Partial', 'Partial'),
    ('Paid',    'Paid'),
    ('Waived',  'Waived'),
]

ATTENDANCE_SESSION = [
    ('Morning', 'Morning Roll Call'),
    ('Evening', 'Evening Roll Call'),
    ('Night',   'Night Roll Call'),
]

ATTENDANCE_STATUS = [
    ('Present', 'Present'),
    ('Absent',  'Absent'),
    ('Leave',   'On Leave'),
    ('Out',     'Out Pass'),
]

LEAVE_STATUS = [
    ('Pending',  'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Returned', 'Returned'),
]

GATEPASS_STATUS = [
    ('Open',     'Open'),
    ('Returned', 'Returned'),
    ('Overdue',  'Overdue'),
]

WAITING_STATUS = [
    ('Waiting',   'Waiting'),
    ('Allocated', 'Allocated'),
    ('Cancelled', 'Cancelled'),
]

ADMISSION_STATUS = [
    ('Active',     'Active'),
    ('Vacated',    'Vacated'),
    ('Transferred','Transferred'),
]


# ─── 1. Hostel Master ─────────────────────────────────────────────────────────

class Hostel(models.Model):
    sch          = models.ForeignKey(school, on_delete=models.CASCADE)
    name         = models.CharField(max_length=100)
    code         = models.CharField(max_length=20)
    hostel_type  = models.CharField(max_length=10, choices=HOSTEL_TYPE, default='Boys')
    category     = models.CharField(max_length=60, blank=True, null=True)
    campus       = models.CharField(max_length=80, blank=True, null=True)
    address      = models.TextField(blank=True, null=True)
    contact      = models.CharField(max_length=15, blank=True, null=True)
    email        = models.EmailField(blank=True, null=True)
    capacity     = models.PositiveIntegerField(default=0)
    warden       = models.CharField(max_length=80, blank=True, null=True)
    warden_mobile= models.CharField(max_length=15, blank=True, null=True)
    status       = models.CharField(max_length=10, choices=HOSTEL_STATUS, default='Active')
    description  = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def total_beds(self):
        return Bed.objects.filter(room__block__hostel=self).count()

    def occupied_beds(self):
        return Bed.objects.filter(room__block__hostel=self, status='Occupied').count()

    def available_beds(self):
        return self.total_beds() - self.occupied_beds()

    def occupancy_percent(self):
        total = self.total_beds()
        if total == 0:
            return 0
        return round((self.occupied_beds() / total) * 100)


# ─── 2. Block / Wing ──────────────────────────────────────────────────────────

class Block(models.Model):
    hostel   = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='blocks')
    name     = models.CharField(max_length=60)
    capacity = models.PositiveIntegerField(default=0)
    floors   = models.PositiveSmallIntegerField(default=1)
    warden   = models.CharField(max_length=80, blank=True, null=True)
    status   = models.CharField(max_length=10, choices=HOSTEL_STATUS, default='Active')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.hostel.name} — {self.name}"


# ─── 3. Floor ─────────────────────────────────────────────────────────────────

FLOOR_NAME_MAP = {
    0: 'Ground Floor', 1: 'First Floor', 2: 'Second Floor',
    3: 'Third Floor',  4: 'Fourth Floor', 5: 'Fifth Floor',
}


class Floor(models.Model):
    block        = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='floor_set')
    floor_number = models.PositiveSmallIntegerField(default=0)
    floor_name   = models.CharField(max_length=40, blank=True, null=True)
    total_rooms  = models.PositiveSmallIntegerField(default=0)
    capacity     = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['floor_number']
        unique_together = ('block', 'floor_number')

    def __str__(self):
        name = self.floor_name or FLOOR_NAME_MAP.get(self.floor_number, f'Floor {self.floor_number}')
        return f"{self.block.name} — {name}"

    def display_name(self):
        return self.floor_name or FLOOR_NAME_MAP.get(self.floor_number, f'Floor {self.floor_number}')

    def save(self, *args, **kwargs):
        if not self.floor_name:
            self.floor_name = FLOOR_NAME_MAP.get(self.floor_number, f'Floor {self.floor_number}')
        super().save(*args, **kwargs)


# ─── 4. Room ──────────────────────────────────────────────────────────────────

class Room(models.Model):
    block       = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='rooms')
    floor       = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms', null=True, blank=True)
    room_number = models.CharField(max_length=20)
    room_type   = models.CharField(max_length=20, choices=ROOM_TYPE, default='Double')
    capacity    = models.PositiveSmallIntegerField(default=2)
    status      = models.CharField(max_length=15, choices=ROOM_STATUS, default='Available')

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"Room {self.room_number} ({self.block.name})"

    def occupied_beds(self):
        return self.beds.filter(status='Occupied').count()

    def available_beds(self):
        return self.beds.filter(status='Available').count()

    def refresh_status(self):
        avail = self.available_beds()
        if avail == 0:
            self.status = 'Full'
        elif self.status == 'Full':
            self.status = 'Available'
        self.save(update_fields=['status'])


# ─── 5. Bed ───────────────────────────────────────────────────────────────────

class Bed(models.Model):
    room       = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    status     = models.CharField(max_length=15, choices=BED_STATUS, default='Available')

    class Meta:
        ordering = ['bed_number']
        unique_together = ('room', 'bed_number')

    def __str__(self):
        return f"Bed {self.bed_number} / Room {self.room.room_number} / {self.room.block.name}"


# ─── 6. Student Hostel Admission ──────────────────────────────────────────────

class HostelAdmission(models.Model):
    sch               = models.ForeignKey(school, on_delete=models.CASCADE)
    student           = models.ForeignKey(students, on_delete=models.CASCADE)
    hostel            = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    block             = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)
    floor             = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    room              = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed               = models.ForeignKey(Bed, on_delete=models.CASCADE)
    admission_date    = models.DateField()
    vacate_date       = models.DateField(null=True, blank=True)
    ac_year           = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    medical_notes     = models.TextField(blank=True, null=True)
    parent_contact    = models.CharField(max_length=15, blank=True, null=True)
    status            = models.CharField(max_length=15, choices=ADMISSION_STATUS, default='Active')
    remarks           = models.TextField(blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.student} → {self.bed}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'Active':
            self.bed.status = 'Occupied'
            self.bed.save(update_fields=['status'])
            self.room.refresh_status()
        elif self.status in ('Vacated', 'Transferred'):
            self.bed.status = 'Available'
            self.bed.save(update_fields=['status'])
            self.room.refresh_status()


# ─── 7. Room / Bed Transfer ───────────────────────────────────────────────────

class RoomTransfer(models.Model):
    sch           = models.ForeignKey(school, on_delete=models.CASCADE)
    student       = models.ForeignKey(students, on_delete=models.CASCADE)
    from_bed      = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='transfers_out')
    to_bed        = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='transfers_in')
    transfer_date = models.DateField()
    reason        = models.TextField()
    approved_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transfer_date']

    def __str__(self):
        return f"{self.student} | {self.from_bed} → {self.to_bed} | {self.transfer_date}"


# ─── 8. Waiting List ──────────────────────────────────────────────────────────

class WaitingList(models.Model):
    sch            = models.ForeignKey(school, on_delete=models.CASCADE)
    student        = models.ForeignKey(students, on_delete=models.CASCADE)
    hostel         = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_type      = models.CharField(max_length=20, choices=ROOM_TYPE, blank=True, null=True)
    priority       = models.PositiveSmallIntegerField(default=1)
    status         = models.CharField(max_length=15, choices=WAITING_STATUS, default='Waiting')
    requested_date = models.DateField()
    remarks        = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['priority', 'requested_date']

    def __str__(self):
        return f"{self.student} waiting for {self.hostel}"


# ─── 9. Hostel Fee Type ───────────────────────────────────────────────────────

class HostelFeeType(models.Model):
    sch        = models.ForeignKey(school, on_delete=models.CASCADE)
    hostel     = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='fee_types')
    name       = models.CharField(max_length=80)
    amount     = models.DecimalField(max_digits=10, decimal_places=2)
    fee_period = models.CharField(max_length=15, choices=FEE_PERIOD, default='Monthly')
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.hostel.name})"


# ─── 10. Hostel Fee Invoice ───────────────────────────────────────────────────

class HostelFeeInvoice(models.Model):
    sch         = models.ForeignKey(school, on_delete=models.CASCADE)
    student     = models.ForeignKey(students, on_delete=models.CASCADE)
    admission   = models.ForeignKey(HostelAdmission, on_delete=models.CASCADE, related_name='invoices')
    fee_type    = models.ForeignKey(HostelFeeType, on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    discount    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issued_date = models.DateField()
    due_date    = models.DateField()
    ac_year     = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    status      = models.CharField(max_length=10, choices=INVOICE_STATUS, default='Pending')
    invoice_no  = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-issued_date']

    def __str__(self):
        return f"{self.student} — {self.fee_type.name} — {self.status}"

    def net_amount(self):
        return self.amount - self.discount

    def amount_paid(self):
        return sum(r.amount_paid for r in self.receipts.all())

    def balance(self):
        return self.net_amount() - self.amount_paid()


# ─── 11. Hostel Fee Receipt ───────────────────────────────────────────────────

class HostelFeeReceipt(models.Model):
    invoice      = models.ForeignKey(HostelFeeInvoice, on_delete=models.CASCADE, related_name='receipts')
    receipt_no   = models.CharField(max_length=20)
    receipt_date = models.DateField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE, default='Cash')
    amount_paid  = models.DecimalField(max_digits=10, decimal_places=2)
    note         = models.CharField(max_length=200, blank=True, null=True)
    received_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-receipt_date']

    def __str__(self):
        return f"Receipt {self.receipt_no} — {self.invoice.student}"


# ─── 12. Hostel Attendance ────────────────────────────────────────────────────

class HostelAttendance(models.Model):
    sch       = models.ForeignKey(school, on_delete=models.CASCADE)
    hostel    = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    student   = models.ForeignKey(students, on_delete=models.CASCADE)
    date      = models.DateField()
    session   = models.CharField(max_length=10, choices=ATTENDANCE_SESSION, default='Night')
    status    = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='Present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date', 'session')
        ordering        = ['student__first_name']

    def __str__(self):
        return f"{self.student} | {self.date} {self.session} | {self.status}"


# ─── 13. Leave Application ────────────────────────────────────────────────────

class LeaveApplication(models.Model):
    sch               = models.ForeignKey(school, on_delete=models.CASCADE)
    student           = models.ForeignKey(students, on_delete=models.CASCADE)
    hostel            = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    from_date         = models.DateField()
    to_date           = models.DateField()
    reason            = models.TextField()
    destination       = models.CharField(max_length=150, blank=True, null=True)
    contact_away      = models.CharField(max_length=15, blank=True, null=True)
    status            = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    applied_on        = models.DateField(auto_now_add=True)
    approved_by       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    parent_notified   = models.BooleanField(default=False)
    actual_return     = models.DateField(null=True, blank=True)
    rejection_reason  = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-applied_on']

    def __str__(self):
        return f"{self.student} | {self.from_date} to {self.to_date} | {self.status}"

    def days(self):
        return (self.to_date - self.from_date).days + 1


# ─── 14. Gate Pass ────────────────────────────────────────────────────────────

class GatePass(models.Model):
    sch             = models.ForeignKey(school, on_delete=models.CASCADE)
    student         = models.ForeignKey(students, on_delete=models.CASCADE)
    hostel          = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    pass_number     = models.CharField(max_length=20)
    out_datetime    = models.DateTimeField()
    expected_return = models.DateTimeField()
    actual_return   = models.DateTimeField(null=True, blank=True)
    purpose         = models.CharField(max_length=200)
    approved_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status          = models.CharField(max_length=10, choices=GATEPASS_STATUS, default='Open')

    class Meta:
        ordering = ['-out_datetime']

    def __str__(self):
        return f"GP-{self.pass_number} | {self.student} | {self.status}"
