from django.db import models
from institutions.models import school

# Create your models here.


from staff.models import staff

class BioDevices(models.Model):
    BioName = models.CharField(max_length=60)
    BioLocation = models.CharField(max_length=50)
    BioSerial = models.CharField(max_length=50)
    BioSchool = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.BioSerial

class BioShift(models.Model):
    ShiftName = models.CharField(max_length=50)
    ShiftStartTime = models.TimeField()
    ShiftEndTime = models.TimeField()
    ShiftSchool = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.ShiftName

class BioDept(models.Model):
    DeptName = models.CharField(max_length=50)
    ShiftDet = models.ForeignKey(BioShift,on_delete=models.CASCADE)
    DeptSchool = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.DeptName

class Employee(models.Model):
    EmployeeId = models.BigIntegerField(primary_key=True)
    EmployeeName_id = models.CharField(max_length=50)
    EmployeeCode = models.CharField(max_length=50)
    StringCode = models.CharField(max_length=50)
    NumericCode = models.BigIntegerField()
    Gender = models.CharField(max_length=10)
    CompanyId = models.BigIntegerField()
    DepartmentId = models.IntegerField()
    Dept = models.ForeignKey(BioDept,on_delete=models.CASCADE,default=1)
    Designation = models.CharField(max_length=255, blank=True)
    CategoryId = models.BigIntegerField()
    DOJ = models.DateTimeField()
    DOR = models.DateTimeField(null=True, blank=True)
    DOC = models.DateTimeField(null=True, blank=True)
    EmployeeCodeInDevice = models.CharField(max_length=50)
    EmployeeRFIDNumber = models.CharField(max_length=50, blank=True)
    EmployementType = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)
    EmployeeDevicePassword = models.CharField(max_length=255, blank=True)
    EmployeeDeviceGroup = models.CharField(max_length=255, blank=True)
    FatherName = models.CharField(max_length=255, blank=True)
    MotherName = models.CharField(max_length=255, blank=True)
    ResidentialAddress = models.TextField(blank=True)
    PermanentAddress = models.TextField(blank=True)
    ContactNo = models.CharField(max_length=50, blank=True)
    Email = models.EmailField(max_length=255, blank=True)
    DOB = models.DateField(null=True, blank=True)
    PlaceOfBirth = models.CharField(max_length=255, blank=True)
    Nomenee1 = models.CharField(max_length=255, blank=True)
    Nomenee2 = models.CharField(max_length=255, blank=True)
    Remarks = models.TextField(blank=True)
    RecordStatus = models.IntegerField()
    C1 = models.CharField(max_length=255, blank=True)
    C2 = models.CharField(max_length=255, blank=True)
    C3 = models.CharField(max_length=255, blank=True)
    C4 = models.CharField(max_length=255, blank=True)
    C5 = models.CharField(max_length=255, blank=True)
    C6 = models.CharField(max_length=255, blank=True)
    C7 = models.CharField(max_length=255, blank=True)
    Location = models.CharField(max_length=255, blank=True)
    BloodGroup = models.CharField(max_length=10, blank=True)
    Workplace = models.CharField(max_length=255, blank=True)
    ExtensionNo = models.CharField(max_length=50, blank=True)
    LoginName = models.CharField(max_length=50, blank=True)
    LoginPassword = models.CharField(max_length=255, blank=True)
    Grade = models.CharField(max_length=50, blank=True)
    Team = models.CharField(max_length=255, blank=True)
    IsRecieveNotification = models.BooleanField(default=False)
    HolidayGroup = models.CharField(max_length=255, blank=True)
    ShiftGroupId = models.BigIntegerField(null=True, blank=True)
    ShiftRosterId = models.BigIntegerField(null=True, blank=True)
    LastModifiedBy = models.CharField(max_length=50, blank=True)
    EmpSchool = models.ForeignKey(school,on_delete=models.CASCADE,default=4)

    class Meta:
        managed = True  # This tells Django not to manage the table
        db_table = 'employees'  # Replace with the actual table name

    def __str__(self):
        return self.EmployeeName_id




class BiometricLog(models.Model):
    DeviceLogId = models.BigAutoField(primary_key=True)
    DownloadDate = models.DateTimeField()
    DeviceId = models.IntegerField()
    UserId = models.IntegerField()
    LogDate = models.DateTimeField()
    Direction = models.CharField(max_length=10)
    AttDirection = models.CharField(max_length=10)
    C1 = models.IntegerField()
    C2 = models.IntegerField()
    C3 = models.IntegerField()
    C4 = models.IntegerField()
    C5 = models.IntegerField()
    C6 = models.IntegerField()
    C7 = models.IntegerField()
    WorkCode = models.IntegerField()
    hrapp_syncstatus = models.IntegerField()

    class Meta:
        managed = False  # We let the external system handle table creation
        db_table = ''  # This will be dynamically set
        app_label = 'biometrics'

    @classmethod
    def set_table_name(cls, table_name):
        """Sets the table name dynamically."""
        cls._meta.db_table = table_name


# Helper function to generate the correct table name
def get_biometric_table_for_month(date=None):
    if not date:
        date = datetime.date.today()
    # Table name format: devicelogs_<month>_<year>
    return f"devicelogs_{date.month}_{date.year}"

class DeviceList(models.Model):
    DeviceId = models.AutoField(primary_key=True)  # AUTO_INCREMENT equivalent
    DeviceFName = models.CharField(max_length=255)  # NOT NULL
    DevicesName = models.CharField(max_length=255)  # NOT NULL
    DeviceDirection = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    SerialNumber = models.CharField(max_length=255)  # NOT NULL
    ConnectionType = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    IpAddress = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    BaudRate = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    CommKey = models.CharField(max_length=255)  # NOT NULL
    ComPort = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    LastLogDownloadDate = models.DateTimeField(null=True, blank=True)  # DEFAULT NULL
    C1 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C2 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C3 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C4 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C5 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C6 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    C7 = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    TransactionStamp = models.CharField(max_length=50, null=True, blank=True)  # DEFAULT NULL
    LastPing = models.DateTimeField(null=True, blank=True)  # DEFAULT NULL
    DeviceType = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    OpStamp = models.CharField(max_length=255, null=True, blank=True)  # DEFAULT NULL
    DownLoadType = models.IntegerField(null=True, blank=True)  # DEFAULT NULL
    TimeZone = models.CharField(max_length=50, null=True, blank=True)  # DEFAULT NULL
    DeviceLocation = models.CharField(max_length=50, null=True, blank=True)  # DEFAULT NULL
    TimeOut = models.CharField(max_length=50, null=True, blank=True)  # DEFAULT NULL

    class Meta:
        managed=False
        db_table = 'devices'
        unique_together = ('DeviceId', 'SerialNumber')  # Equivalent to primary key combination

    def __str__(self):
        return f"{self.DeviceFName} ({self.SerialNumber})"
from django.db import models


