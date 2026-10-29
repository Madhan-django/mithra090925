from django.db import models
from django.contrib.auth.models import Group



class school(models.Model):
    name = models.CharField('school', max_length=50)
    phone = models.CharField('phone', max_length=11)
    email = models.EmailField()
    website = models.CharField(max_length=80,blank=True,null=True)
    address = models.TextField('address', max_length=150)
    logo = models.ImageField(upload_to='logos/',blank=True,null=True)
    notification_logo= models.ImageField(upload_to='logos/',blank=True,null=True)
    group_code = models.CharField( max_length=10,blank=True,null=True)
    regno = models.CharField(max_length=50)
    isactive=models.BooleanField()
    web_aboutus = models.CharField(max_length=80,blank=True,null=True)
    web_contactus = models.CharField(max_length=80,blank=True,null=True)
    web_gallery = models.CharField(max_length=80,blank=True,null=True)
    web_admission = models.CharField(max_length=80,blank=True,null=True)

    def __str__(self):
        return self.name


class SchoolMenuPermission(models.Model):
    school        = models.OneToOneField(school, on_delete=models.CASCADE, related_name='menu_permission')
    admission     = models.BooleanField(default=True)
    students      = models.BooleanField(default=True)
    staffs        = models.BooleanField(default=True)
    academics     = models.BooleanField(default=True)
    timetable     = models.BooleanField(default=True)
    finance       = models.BooleanField(default=True)
    payroll       = models.BooleanField(default=True)
    transport     = models.BooleanField(default=True)
    hostel        = models.BooleanField(default=True)
    petty_cash    = models.BooleanField(default=True)
    examination   = models.BooleanField(default=True)
    question_bank = models.BooleanField(default=True)
    library       = models.BooleanField(default=True)
    assets        = models.BooleanField(default=True)
    inventory     = models.BooleanField(default=True)
    visitors      = models.BooleanField(default=True)
    reports       = models.BooleanField(default=True)
    jacob_reports = models.BooleanField(default=False)
    certificates  = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.school.name} – Menu Permissions"

    class Meta:
        verbose_name = "School Menu Permission"
        verbose_name_plural = "School Menu Permissions"


class GroupMenuPermission(models.Model):
    """Controls which sidebar sections each Django Group can access, per school."""
    group  = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='school_menu_permissions')
    school = models.ForeignKey(school, on_delete=models.CASCADE, related_name='group_menu_permissions')

    # Module visibility — combined AND with SchoolMenuPermission
    admission      = models.BooleanField(default=True)
    students       = models.BooleanField(default=True)
    staffs         = models.BooleanField(default=True)
    academics      = models.BooleanField(default=True)
    timetable      = models.BooleanField(default=True)
    finance        = models.BooleanField(default=False)
    payroll        = models.BooleanField(default=False)
    transport      = models.BooleanField(default=False)
    hostel         = models.BooleanField(default=False)
    petty_cash     = models.BooleanField(default=False)
    examination    = models.BooleanField(default=True)
    question_bank  = models.BooleanField(default=False)
    library        = models.BooleanField(default=True)
    assets         = models.BooleanField(default=False)
    inventory      = models.BooleanField(default=False)
    visitors       = models.BooleanField(default=False)
    reports        = models.BooleanField(default=False)
    jacob_reports  = models.BooleanField(default=False)
    certificates   = models.BooleanField(default=False)

    # Admin-level sub-features
    configurations        = models.BooleanField(default=False, help_text="Settings/Configurations sidebar section")
    students_authenticate = models.BooleanField(default=False, help_text="Student login credential management")
    students_promote      = models.BooleanField(default=False, help_text="Student class promotion")
    students_transfer     = models.BooleanField(default=False, help_text="Student transfer")

    def __str__(self):
        return f"{self.group.name} @ {self.school.name}"

    class Meta:
        verbose_name = "Group Menu Permission"
        verbose_name_plural = "Group Menu Permissions"
        unique_together = ('group', 'school')