from django.db import models
from django.db.models import SET_NULL
from django.contrib.auth.models import User

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
BANK_CHOICES = [

    # Public Sector Banks
    ('State Bank of India', 'State Bank of India'),
    ('Punjab National Bank', 'Punjab National Bank'),
    ('Bank of Baroda', 'Bank of Baroda'),
    ('Canara Bank', 'Canara Bank'),
    ('Union Bank of India', 'Union Bank of India'),
    ('Indian Bank', 'Indian Bank'),
    ('Bank of India', 'Bank of India'),
    ('Central Bank of India', 'Central Bank of India'),
    ('Indian Overseas Bank', 'Indian Overseas Bank'),
    ('UCO Bank', 'UCO Bank'),
    ('Bank of Maharashtra', 'Bank of Maharashtra'),
    ('Punjab & Sind Bank', 'Punjab & Sind Bank'),

    # Private Sector Banks
    ('HDFC Bank', 'HDFC Bank'),
    ('ICICI Bank', 'ICICI Bank'),
    ('Axis Bank', 'Axis Bank'),
    ('Kotak Mahindra Bank', 'Kotak Mahindra Bank'),
    ('IndusInd Bank', 'IndusInd Bank'),
    ('IDFC First Bank', 'IDFC First Bank'),
    ('Federal Bank', 'Federal Bank'),
    ('RBL Bank', 'RBL Bank'),
    ('Bandhan Bank', 'Bandhan Bank'),
    ('South Indian Bank', 'South Indian Bank'),
    ('Yes Bank', 'Yes Bank'),

    # Small Finance Banks
    ('AU Small Finance Bank', 'AU Small Finance Bank'),
    ('Ujjivan Small Finance Bank', 'Ujjivan Small Finance Bank'),
    ('Equitas Small Finance Bank', 'Equitas Small Finance Bank'),
    ('ESAF Small Finance Bank', 'ESAF Small Finance Bank'),
    ('Suryoday Small Finance Bank', 'Suryoday Small Finance Bank'),

    # Payments Banks
    ('India Post Payments Bank', 'India Post Payments Bank'),
    ('Airtel Payments Bank', 'Airtel Payments Bank'),
    ('Paytm Payments Bank', 'Paytm Payments Bank'),
]

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class PayrollEmployee(models.Model):
    employee = models.ForeignKey(staff, on_delete=models.CASCADE)
    school = models.ForeignKey(school, on_delete=models.CASCADE)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)

    # salary breakup
    basic_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=70)
    hra_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    wages_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}"


class PayrollBank(models.Model):
    CustName = models.ForeignKey(staff,on_delete=models.CASCADE)
    home_school = models.ForeignKey(school,on_delete=models.CASCADE)
    AccNo = models.CharField(max_length=25)
    CIFNo = models.CharField(max_length=25,blank=True,null=True)
    BankName = models.CharField(choices=BANK_CHOICES,max_length=100)
    Branch = models.CharField(max_length=25)
    IFSC = models.CharField(max_length=13)

    def __str__(self):
        return self.CustName.first_name+ " "+self.CustName.last_name




class Allowance(models.Model):
    name = models.CharField(max_length=100)
    allow_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Deductions(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class staff_deduction(models.Model):
    name = models.ForeignKey(Deductions,on_delete=SET_NULL,null=True)
    staff = models.ForeignKey(staff,on_delete=SET_NULL,null=True)
    ded_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    sch = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee_name.name} - {self.deduction_name.name}"






class Employee_allowance_Details(models.Model):
    employee_name = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    allowance_name = models.ForeignKey(Allowance,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.employee.name}"





class Loan(models.Model):
    employee = models.ForeignKey(staff, on_delete=models.CASCADE)
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

class PayrollMonthly(models.Model):
    employee = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE)
    school = models.ForeignKey(school, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()
    total_lop_days = models.DecimalField(max_digits=5, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_sal_month = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    basic_da = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    esi = models.DecimalField(max_digits=10, decimal_places=2)
    pf= models.DecimalField(max_digits=10, decimal_places=2)
    ded = models.DecimalField(max_digits=10, decimal_places=2)
    total_ded = models.DecimalField(max_digits=10, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)
    total_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    working_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    salary_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_finalized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'month', 'year')

class PayrollBankReconciliation(models.Model):
    school = models.ForeignKey(school, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()

    payroll_total = models.DecimalField(max_digits=12, decimal_places=2)
    bank_total = models.DecimalField(max_digits=12, decimal_places=2)
    difference = models.DecimalField(max_digits=12, decimal_places=2)

    reconciled_on = models.DateTimeField(auto_now_add=True)
    reconciled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    is_locked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('school', 'month', 'year')

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
    Sandwich_Leave_Policy = models.BooleanField(default=False)
    half_day_as_cl = models.BooleanField(default=False)
    saturday_short_day = models.BooleanField(default=False)
    # Late Settings
    grace_late_count = models.PositiveIntegerField(default=3)
    grace_mins = models.PositiveIntegerField(default=0)
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

class StatutorySettings(models.Model):
    sch = models.OneToOneField(school, on_delete=models.CASCADE)

    # PF
    pf_employee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=12)
    pf_employer_percent = models.DecimalField(max_digits=5, decimal_places=2, default=12)
    pf_basic_limit = models.DecimalField(max_digits=10, decimal_places=2, default=15000)

    # ESI
    esi_employee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.75)
    esi_employer_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3.25)
    esi_gross_limit = models.DecimalField(max_digits=10, decimal_places=2, default=21000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sch.name} Statutory Settings"

