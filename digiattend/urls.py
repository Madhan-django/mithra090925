from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.log_list), name='log_list'),
    path('NewBioDevices',login_required(views.NewBioDevices),name='NewBioDevices'),
    path('DeviceList',login_required(views.BioDeviceList),name='DeviceList'),
    path('BioDeviceDelete/<Biodev_id>',login_required(views.BioDeviceDelete),name='BioDeviceDelete'),
    path('NewShift',login_required(views.NewShift),name='NewShift'),
    path('NewDept',login_required(views.NewDept),name='NewDept'),
    path('employeelist',login_required(views.employeelist),name='employeelist'),
    path('employeeUpdate/<emp_id>',login_required(views.employeeUpdate),name='employeeUpdate'),
    path('NewEmployee',login_required(views.NewEmployee),name='NewEmployee')

]


