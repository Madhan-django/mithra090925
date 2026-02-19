from django.db import models
from institutions.models import school
from staff.models import staff
import datetime
from django.utils import timezone
from datetime import date

# Create your models here.
ded_from =[
    ('Gross','Gross'),
    ('Basic','Basic')

]


Hol =[
    ('Weekly-OFF','Weekly-OFF'),
    ('Special-OFF','Special-OFF')

]


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PayrollEmployee(models.Model):
    emp_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    emp_type = models.CharField(max_length=25,default=1)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.BooleanField(default=True)  # Active/Inactive
    emp_sch = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PayrollBank(models.Model):
    CustName = models.ForeignKey(PayrollEmployee,on_delete=models.CASCADE)
    AccNo = models.CharField(max_length=25)
    CIFNo = models.CharField(max_length=25,blank=True,null=True)
    BankName = models.CharField(max_length=100)
    Branch = models.CharField(max_length=25)
    IFSC = models.CharField(max_length=10)

    def __str__(self):
        return self.CustName




class Allowance(models.Model):
    name = models.CharField(max_length=100)
    allow_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Deduction(models.Model):
    METHOD_CHOICES = [
        ('percentage_basic', 'Percentage of Basic Salary'),
        ('percentage_gross', 'Percentage of Gross Salary'),
        ('fixed_amount', 'Fixed Monthly Amount'),
        ('emi', 'EMI Based Deduction'),
    ]

    CEIL_BASED_ON_CHOICES = [
        ('basic', 'Basic Salary'),
        ('gross', 'Gross Salary'),
    ]

    name = models.CharField(max_length=100, unique=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage or fixed")
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=date(2900, 1, 1))

    # NEW: Ceiling limits based on salary type
    ciel_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Min salary to apply this deduction")
    ciel_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Max salary to apply this deduction")
    ciel_based_on = models.CharField(max_length=10, choices=CEIL_BASED_ON_CHOICES, null=True, blank=True, help_text="Check ceiling based on Basic/Gross salary")
    sch = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.method})"



class Employee_allowance_Details(models.Model):
    employee_name = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    allowance_name = models.ForeignKey(Allowance,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.employee.name}"



class Employee_deduction_Details(models.Model):
    employee_name = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    deduction_name = models.ForeignKey(Deduction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_name.name} - {self.deduction_name.name}"

class Loan(models.Model):
    employee = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    loan_name = models.CharField(max_length=25)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(default=datetime.date(1900, 1, 1))

    def __str__(self):
        return f"Loan {self.employee.name}"

class PayrollPeriod(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    sch = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.month}/{self.year}"

class Payslip(models.Model):
    employee = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    total_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sch = models.ForeignKey(school, on_delete=models.CASCADE)
    def __str__(self):
        return f"Payslip {self.employee.name} - {self.period}"

class tempattend(models.Model):
    employee = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    days = models.DecimalField(max_digits=3, decimal_places=1, default=0)




class Attendance(models.Model):
    STATUS_CHOICES = (
        ("PRESENT", "Present"),
        ("ABSENT", "Absent"),
        ("HALF_DAY", "Half Day"),
        ("MIS_PUNCH", "Miss Punch"),

        # 🔥 Leave Types
        ("CL", "Casual Leave"),
        ("ML", "Medical Leave"),
        ("PERMISSION", "Permission"),
        ("LOP", "Loss of Pay"),

        # 🔥 Special Days
        ("HOLIDAY", "Holiday"),

    )

    sch = models.ForeignKey(school, on_delete=models.CASCADE)
    staff = models.ForeignKey(staff,on_delete=models.CASCADE)


    date = models.DateField()

    # ========== RAW DEVICE DATA ==========
    first_in = models.DateTimeField(null=True, blank=True)
    last_out = models.DateTimeField(null=True, blank=True)
    punch_count = models.IntegerField(default=0)

    # ========== CALCULATED VALUES ==========
    work_duration = models.DurationField(null=True, blank=True)
    late_minutes = models.IntegerField(default=0)

    # ========== FLAGS ==========
    late = models.BooleanField(default=False)
    mis_punch = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)  # HR edited

    # ========== FINAL STATUS ==========
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PRESENT"
    )

    leave_type = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)

    # ========== PAYROLL LOCK ==========
    is_finalized = models.BooleanField(default=False)

    # ========== SYSTEM FIELDS ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('staff', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['staff']),
        ]

    def __str__(self):
        return f"{self.staff} - {self.date} - {self.status}"


class Holiday(models.Model):
    sch = models.ForeignKey(school, on_delete=models.CASCADE)
    date = models.DateField()
    name = models.CharField(max_length=20,choices=Hol)

    class Meta:
        unique_together = ('sch', 'date')

    def __str__(self):
        return f"{self.date} - {self.name}"

class LeaveBalance(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    year = models.IntegerField()
    cl_balance = models.DecimalField(max_digits=4, decimal_places=1, default=12)
    ml_balance = models.DecimalField(max_digits=4, decimal_places=1, default=10)

    class Meta:
        unique_together = ('staff', 'year')


class PayrollSettings(models.Model):

    PAYROLL_MONTH_CHOICES = [
        ("JAN-DEC", "JAN - DEC"),
        ("JUN-MAY", "JUN - MAY"),
        ("APR-MAR", "APR - MAR"),
    ]

    school = models.OneToOneField(
        school,
        on_delete=models.CASCADE,
        related_name="payroll_settings"
    )

    payroll_date = models.PositiveIntegerField(default=5)  # 5th of every month

    payroll_month_cycle = models.CharField(
        max_length=20,
        choices=PAYROLL_MONTH_CHOICES,
        default="JUN-MAY"
    )

    # Leave Settings
    total_cl = models.PositiveIntegerField(default=12)
    cl_per_month = models.PositiveIntegerField(default=1)
    allow_previous_cl_usage = models.BooleanField(default=True)

    total_ml = models.PositiveIntegerField(default=3)

    # Late Settings
    grace_late_count = models.PositiveIntegerField(default=3)
    lop_after_grace = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.25
    )

    late_cutoff_hour = models.PositiveIntegerField(default=9)

    # Permission Settings
    permission_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.0
    )

    permission_per_month = models.PositiveIntegerField(default=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.name} Payroll Settings"
