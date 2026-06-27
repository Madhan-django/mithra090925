from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('department', login_required(views.PDept_list), name='department'),
    path('add_depts', login_required(views.PDept_add), name='add_depts'),
    path('PDept_update/<dept_id>', login_required(views.PDept_update), name='update_deptss'),
    path('PDept_del/<dept_id>', login_required(views.PDept_del), name='del_dept'),

    path('', login_required(views.PEmployees), name='Employees'),
    path('add_Employee', login_required(views.PEmployee_add), name='add_Employee'),
    path('update_Employee/<emp_id>', login_required(views.PEmployee_update), name='update_Employee'),
    path('del_Employee/<emp_id>', login_required(views.PEmployee_del), name='del_Employee'),

    path('allowance', login_required(views.Allowance_list), name='allowance'),
    path('add_allowance', login_required(views.add_Allowance), name='add_allowance'),
    path('update_Allowance/<allowance_id>', login_required(views.update_Allowance), name='update_Allowance'),
    path('del_Allowance/<allowance_id>', login_required(views.del_Allowance), name='del_Allowance'),
    path('apply_allowance/<allowance_id>', login_required(views.apply_Allowance), name='apply_allowance'),
    path('deductions', login_required(views.Deduction_list), name='deductions'),
    path('add_deduction', login_required(views.add_Deduction), name='add_deduction'),
    path('update_Deduction/<deduction_id>', login_required(views.update_Deduction), name='update_Deduction'),
    path('del_Deduction/<deduction_id>', login_required(views.del_Deduction), name='del_Deduction'),
    path('staff_deduction_list',login_required(views.staff_deduction_list),name='staff_deduction_list'),
    path('add_staff_deduction',login_required(views.add_staff_deduction), name='add_staff_deduction'),
    path('del_staff_deduction/<int:ded_id>/', login_required(views.del_staff_deduction), name='del_staff_deduction'),
    path('Salary_Record/<Employee_id>', login_required(views.Employee_Salary_Record), name='Salary_Record'),
    path('update_salary/', login_required(views.update_salary), name='update_salary'),

    path('loan_list', login_required(views.Loan_List), name='loan_list'),
    path('new_loan', login_required(views.New_Loan), name='new_loan'),
    path('del_loan/<loan_id>', login_required(views.Del_Loan), name='del_loan'),

    path('day_attendance', login_required(views.daily_attendance_view), name='day_attendance'),
    path('day_attendance/excel/', views.daily_attendance_excel, name='daily_attendance_excel'),
    path('import_employees/', login_required(views.import_employees), name='import_employees'),
    path('export_employee_sample', login_required(views.export_employee_sample), name='export_employee_sample'),
    path('fetch_attendance', login_required(views.sync_attendance_from_device), name='fetch_attendance'),
    path('sync_attendance',login_required(views.force_sync_attendance_from_device),name='sync_attendance'),

    path('Staff_Monthly_Attendance', login_required(views.Staff_Monthly_Attendance), name='Staff_Monthly_Attendance'),
    path('toggle_late_exemption/<int:attendance_id>/', login_required(views.toggle_late_exemption), name='toggle_late_exemption'),
    path('attendance-register/', login_required(views.attendance_register), name='attendance_register'),
    path('delete_all_attendance',login_required(views.delete_all_attendance), name='delete_all_attendance'),
    path('Staff_Monthly_Summary', login_required(views.staff_monthly_summary), name='Staff_Monthly_Summary'),
    path('Staff_Monthly_Summary_Excel', login_required(views.staff_monthly_summary_excel), name='Staff_Monthly_Summary_Excel'),

    path('holidays', login_required(views.Holiday_List), name='Holidays'),
    path('add_holiday', login_required(views.add_holiday), name='add_holiday'),
    path('holiday/<int:id>', login_required(views.delete_holiday), name='delete_holiday'),
    path('reapply_holidays_attendance', login_required(views.reapply_holidays_attendance), name='reapply_holidays_attendance'),

    path('psettings', login_required(views.PayrollSet), name='psettings'),
    path('create_payroll_settings', login_required(views.create_payroll_settings), name='create_payroll_settings'),
    path('edit_payroll_settings', login_required(views.edit_payroll_settings), name='edit_payroll_settings'),
    path('delete_payroll_settings', login_required(views.delete_payroll_settings), name='delete_payroll_settings'),

    path('generate_payroll', login_required(views.generate_payroll), name='generate_payroll'),
    path('payroll_register', login_required(views.payroll_register), name='payroll_register'),
    path("payroll-register/export/", login_required(views.payroll_register_excel), name="payroll_register_excel"),

    path("statutory/", login_required(views.statutory_settings_list), name="statutory_settings_list"),
    path("statutory/add/", login_required(views.statutory_settings_add), name="statutory_settings_add"),
    path('statutory/edit/', login_required(views.statutory_settings_edit), name='statutory_settings_edit'),
    path("statutory/delete/", login_required(views.statutory_settings_delete), name="statutory_settings_delete"),
    path("bank_details/",login_required(views.bank_details), name="bank_details"),
    path("add_bank_record/",login_required(views.add_bank_record),name="add_bank_record"),
    path('edit_bank_record/<int:rec_id>/',login_required(views.edit_bank_record),name='edit_bank_record'),
    path('delete_bank_record/<int:rec_id>/',login_required(views.delete_bank_record),name='delete_bank_record'),
    path('bank_statement',login_required(views.payroll_bank_statement),name='bank_statement'),
    path('export_bank_statement/', views.export_bank_statement, name='export_bank_statement'),
]

