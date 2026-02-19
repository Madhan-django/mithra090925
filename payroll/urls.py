from django.urls import path
from . import views

urlpatterns=[
    path('department',views.PDept_list,name='department'),
    path('add_depts',views.PDept_add,name='add_depts'),
    path('PDept_update/<dept_id>',views.PDept_update,name='update_dept'),
    path('PDept_del/<dept_id>',views.PDept_del,name='del_dept'),
    path('designation',views.PDesignation_list,name='designation'),
    path('add_desg',views.PDesignation_add,name='add_desg'),
    path('update_desg/<desg_id>',views.PDesignation_update,name='update_desg'),
    path('del_desg/<desg_id>',views.PDesignation_del,name='del_desg'),
    path('',views.PEmployees,name='Employees'),
    path('add_Employee',views.PEmployee_add,name='add_Employee'),
    path('update_Employee/<emp_id>',views.PEmployee_update,name='update_Employee'),
    path('del_Employee/<emp_id>',views.PEmployee_del,name='del_Employee'),
    path('allowance',views.Allowance_list,name='allowance'),
    path('add_allowance',views.add_Allowance,name='add_allowance'),
    path('update_Allowance/<allowance_id>',views.update_Allowance,name='update_Allowance'),
    path('del_Allowance/<allowance_id>',views.del_Allowance,name='del_Allowance'),
    path('apply_allowance/<allowance_id>',views.apply_Allowance,name='apply_allowance'),
    path('apply_deduction/<deduction_id>',views.apply_Deduction,name='apply_deduction'),
    path('deduction',views.Deduction_list,name='deduction'),
    path('add_deduction',views.add_Deduction,name='add_deduction'),
    path('update_Deduction/<deduction_id>',views.update_Deduction,name='update_Deduction'),
    path('del_Deduction/<deduction_id>',views.del_Deduction,name='del_Deduction'),
    path('Salary_Record/<Employee_id>',views.Employee_Salary_Record,name='Salary_Record'),
    path('update_salary/',views.update_salary, name='update_salary'),
    path('loan_list',views.Loan_List,name='loan_list'),
    path('new_loan',views.New_Loan,name='new_loan'),
    path('del_loan/<loan_id>',views.Del_Loan,name='del_loan'),
    path('day_attendance',views.daily_attendance_view,name='day_attendance'),
    path('import_employees/', views.import_employees, name='import_employees'),
    path('export_employee_sample',views.export_employee_sample,name='export_employee_sample'),
    path('fetch_attendance',views.sync_attendance_from_device,name='fetch_attendance'),
    path('Staff_Monthly_Attendance',views.Staff_Monthly_Attendance,name='Staff_Monthly_Attendance'),
    path('Staff_Monthly_Summary',views.staff_monthly_summary,name='Staff_Monthly_Summary'),
    path('holidays',views.Holiday_List,name='Holidays'),
    path('add_holiday',views.add_holiday,name='add_holiday'),
    path('holiday/<int:id>', views.delete_holiday, name='delete_holiday'),
    path('psettings',views.PayrollSet,name='psettings'),
    path('create_payroll_settings',views.create_payroll_settings,name='create_payroll_settings'),
    path('edit_payroll_settings',views.edit_payroll_settings,name='edit_payroll_settings'),
    path('delete_payroll_settings',views.delete_payroll_settings,name='delete_payroll_settings')



]