from django.db import models
from institutions.models import school
from admission.models import students
from datetime import date, timedelta


FUEL_CHOICES = [
    ('Diesel', 'Diesel'),
    ('Petrol', 'Petrol'),
    ('CNG', 'CNG'),
    ('Electric', 'Electric'),
]

VEHICLE_STATUS = [
    ('Active', 'Active'),
    ('Maintenance', 'Under Maintenance'),
    ('Inactive', 'Inactive'),
]

BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]


class VehicleType(models.Model):
    sch  = models.ForeignKey(school, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    sch            = models.ForeignKey(school, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    vehicle_name   = models.CharField(max_length=60)
    vehicle_type   = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True)
    capacity       = models.PositiveIntegerField(default=40)
    gps_device_id  = models.CharField(max_length=50, blank=True, null=True)
    chassis_number = models.CharField(max_length=50, blank=True, null=True)
    engine_number  = models.CharField(max_length=50, blank=True, null=True)
    fuel_type      = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Diesel')
    purchase_date  = models.DateField(null=True, blank=True)
    rc_number      = models.CharField(max_length=30, blank=True, null=True)

    insurance_expiry  = models.DateField(null=True, blank=True)
    fitness_expiry    = models.DateField(null=True, blank=True)
    permit_expiry     = models.DateField(null=True, blank=True)
    pollution_expiry  = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=VEHICLE_STATUS, default='Active')

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"

    def expiring_soon(self, days=30):
        today  = date.today()
        cutoff = today + timedelta(days=days)
        alerts = []
        docs = [
            ('Insurance',  self.insurance_expiry),
            ('Fitness',    self.fitness_expiry),
            ('Permit',     self.permit_expiry),
            ('Pollution',  self.pollution_expiry),
        ]
        for label, exp in docs:
            if exp and exp <= cutoff:
                delta = (exp - today).days
                alerts.append({'doc': label, 'expiry': exp, 'days_left': delta})
        return alerts


class Driver(models.Model):
    sch               = models.ForeignKey(school, on_delete=models.CASCADE)
    name              = models.CharField(max_length=80)
    employee_id       = models.CharField(max_length=30, blank=True, null=True)
    mobile            = models.CharField(max_length=15)
    address           = models.TextField(blank=True, null=True)
    aadhaar           = models.CharField(max_length=12, blank=True, null=True)
    license_number    = models.CharField(max_length=30)
    license_expiry    = models.DateField()
    blood_group       = models.CharField(max_length=5, choices=BLOOD_GROUPS, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    assigned_vehicle  = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers')
    status            = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return self.name

    def license_expiring_soon(self, days=30):
        today = date.today()
        return self.license_expiry <= today + timedelta(days=days)


class Route(models.Model):
    sch            = models.ForeignKey(school, on_delete=models.CASCADE)
    route_name     = models.CharField(max_length=100)
    route_code     = models.CharField(max_length=20)
    vehicle        = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    driver         = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='routes')
    total_distance = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    is_active      = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.route_code} — {self.route_name}"

    def total_stops(self):
        return self.stops.count()

    def allocated_students(self):
        return StudentTransport.objects.filter(route=self, is_active=True).count()

    def seat_available(self):
        if self.vehicle:
            return self.vehicle.capacity - self.allocated_students()
        return None


class Stop(models.Model):
    route       = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name   = models.CharField(max_length=100)
    area        = models.CharField(max_length=100, blank=True, null=True)
    landmark    = models.CharField(max_length=150, blank=True, null=True)
    pickup_time = models.TimeField(null=True, blank=True)
    drop_time   = models.TimeField(null=True, blank=True)
    sequence    = models.PositiveIntegerField(default=1)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"{self.stop_name} ({self.route.route_code})"

    def student_count(self):
        return StudentTransport.objects.filter(stop=self, is_active=True).count()


class StudentTransport(models.Model):
    sch        = models.ForeignKey(school, on_delete=models.CASCADE)
    student    = models.ForeignKey(students, on_delete=models.CASCADE)
    route      = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop       = models.ForeignKey(Stop, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date   = models.DateField(null=True, blank=True)
    is_active  = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'is_active')

    def __str__(self):
        return f"{self.student} → {self.stop}"


# ─── Boarding Attendance ──────────────────────────────────────────────────────

class BoardingAttendance(models.Model):
    TRIP_CHOICES   = [('AM', 'Morning'), ('PM', 'Evening')]
    STATUS_CHOICES = [
        ('Boarded', 'Boarded'),
        ('Absent',  'Absent'),
        ('Missed',  'Missed Bus'),
    ]

    sch       = models.ForeignKey(school, on_delete=models.CASCADE)
    route     = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop      = models.ForeignKey(Stop, on_delete=models.CASCADE)
    student   = models.ForeignKey(students, on_delete=models.CASCADE)
    date      = models.DateField()
    trip      = models.CharField(max_length=2, choices=TRIP_CHOICES, default='AM')
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Boarded')
    marked_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date', 'trip')
        ordering        = ['stop__sequence', 'student__first_name']

    def __str__(self):
        return f"{self.student} | {self.date} {self.trip} | {self.status}"


# ─── GPS ──────────────────────────────────────────────────────────────────────

class GpsSettings(models.Model):
    """One row per school — stores the Mappls API key for live-map rendering."""
    sch            = models.OneToOneField(school, on_delete=models.CASCADE, related_name='gps_settings')
    mappls_api_key = models.CharField(max_length=100, blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GPS Settings — {self.sch}"


class VehiclePosition(models.Model):
    """Latest known GPS position for each vehicle. One row kept per vehicle (upserted on each push)."""
    vehicle    = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='position')
    latitude   = models.DecimalField(max_digits=10, decimal_places=7)
    longitude  = models.DecimalField(max_digits=10, decimal_places=7)
    speed_kmh  = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    heading    = models.SmallIntegerField(default=0)  # degrees 0-359
    timestamp  = models.DateTimeField()               # timestamp from device
    received_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} @ {self.latitude},{self.longitude}"


class VehiclePositionHistory(models.Model):
    """Full history of position pings — written on every push."""
    vehicle    = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='position_history')
    latitude   = models.DecimalField(max_digits=10, decimal_places=7)
    longitude  = models.DecimalField(max_digits=10, decimal_places=7)
    speed_kmh  = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    heading    = models.SmallIntegerField(default=0)
    timestamp  = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes  = [models.Index(fields=['vehicle', '-timestamp'])]

    def __str__(self):
        return f"{self.vehicle} @ {self.timestamp}"
