from django.contrib import admin
from .models import (
    Department, Designation, PayrollEmployee, PayrollBank,
    Allowance, Deduction,
    Employee_allowance_Details, Employee_deduction_Details,
    Loan, PayrollPeriod, Payslip,
    Attendance, Holiday, LeaveBalance,
    PayrollSettings
)


# ===================== Department =====================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'sch')
    search_fields = ('name',)
    list_filter = ('sch',)


# ===================== Designation =====================
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department')
    search_fields = ('title',)
    list_filter = ('department',)


# ===================== Payroll Employee =====================


# ===================== Payroll Bank =====================
@admin.register(PayrollBank)
class PayrollBankAdmin(admin.ModelAdmin):
    list_display = ('CustName', 'BankName', 'Branch', 'IFSC')
    search_fields = ('CustName__name', 'AccNo', 'IFSC')


# ===================== Allowance =====================
@admin.register(Allowance)
class AllowanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'allow_percentage', 'sch')
    search_fields = ('name',)
    list_filter = ('sch',)


# ===================== Deduction =====================
@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ('name', 'method', 'value', 'start_date', 'end_date', 'sch')
    list_filter = ('method', 'sch')
    search_fields = ('name',)


# ===================== Employee Allowance =====================
@admin.register(Employee_allowance_Details)
class EmployeeAllowanceAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'allowance_name', 'amount')
    list_filter = ('allowance_name',)


# ===================== Employee Deduction =====================
@admin.register(Employee_deduction_Details)
class EmployeeDeductionAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'deduction_name', 'amount', 'emi_amount', 'balance', 'active')
    list_filter = ('deduction_name', 'active')


# ===================== Loan =====================
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'loan_name', 'loan_amount', 'remaining_amount', 'start_date', 'end_date')
    search_fields = ('employee__name', 'loan_name')


# ===================== Payroll Period =====================
@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'sch')
    list_filter = ('year', 'sch')


# ===================== Payslip =====================
@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period', 'net_salary', 'created_at')
    list_filter = ('period', 'sch')
    search_fields = ('employee__name',)


# ===================== Attendance =====================
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status', 'late', 'mis_punch', 'is_finalized')
    list_filter = ('status', 'late', 'mis_punch', 'sch')
    search_fields = ('staff__name',)
    readonly_fields = ('created_at', 'updated_at')


# ===================== Holiday =====================
@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'sch')
    list_filter = ('sch', 'name')


# ===================== Leave Balance =====================
@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'year', 'cl_balance', 'ml_balance')
    list_filter = ('year',)


# ===================== Payroll Settings =====================
@admin.register(PayrollSettings)
class PayrollSettingsAdmin(admin.ModelAdmin):

    list_display = (
        'school',
        'payroll_date',
        'payroll_month_cycle',
        'total_cl',
        'cl_per_month',
        'total_ml',
        'grace_late_count',
        'lop_after_grace'
    )

    list_filter = ('payroll_month_cycle', 'school')
    search_fields = ('school__name',)
    readonly_fields = ('created_at',)

    fieldsets = (

        ("Basic Payroll Settings", {
            'fields': (
                'school',
                'payroll_date',
                'payroll_month_cycle',
            )
        }),

        ("Leave Settings", {
            'fields': (
                'total_cl',
                'cl_per_month',
                'allow_previous_cl_usage',
                'total_ml',
            )
        }),

        ("Late Settings", {
            'fields': (
                'grace_late_count',
                'lop_after_grace',
                'late_cutoff_hour',
            )
        }),

        ("Permission Settings", {
            'fields': (
                'permission_hours',
                'permission_per_month',
            )
        }),

        ("System Info", {
            'fields': ('created_at',)
        }),
    )