from django.db import models
from institutions.models import school
from django.contrib.auth.models import User
from setup.models import currentacademicyr,sclass,section,academicyr
from admission.models import students
import uuid



# Create your models here.
class fees(models.Model):
    invoice_title = models.CharField(max_length=150)
    desc = models.CharField(max_length=250)
    fee_group = models.CharField(max_length=25,null=True,blank=True)
    iclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    issued_date = models.DateField()
    due_date = models.DateField()
    fees_school = models.ForeignKey(school, on_delete=models.CASCADE)
    fee_amount = models.IntegerField()
    ac_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    latefee = models.IntegerField()
    isactive = models.CharField(max_length=3)

    def __str__(self):
        return self.invoice_title

class addindfee(models.Model):
    fee_cat = models.ForeignKey(fees, on_delete=models.CASCADE)
    class_name = models.ForeignKey(sclass, on_delete=models.CASCADE)
    stud_name = models.ForeignKey(students,on_delete=models.CASCADE,blank=True,null=True)

    due_amt = models.IntegerField()
    concession = models.IntegerField()
    concession_apply = models.BooleanField(default=False)
    invoice_no = models.IntegerField()
    status = models.CharField(max_length=15)


    def __str__(self):
        return self.fee_cat.invoice_title


class bulkfee(models.Model):
    fee_cat = models.ForeignKey(fees, on_delete=models.CASCADE)
    class_name = models.ForeignKey(sclass, on_delete=models.CASCADE)
    years = models.ForeignKey(academicyr,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.fee_cat.invoice_title



class fee_reciept(models.Model):
    reciept_date = models.DateField()
    reciept_no = models.IntegerField()
    reciept_inv = models.ForeignKey(addindfee,on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    payment_id= models.CharField(max_length=20,blank=True,null=True)
    total = models.IntegerField(blank=True, null=True)
    paid_amt = models.IntegerField(blank=True, null=True)
    note= models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.payment_type

class del_fee_reciept(models.Model):
    reciept_date = models.DateField()
    deletedate = models.DateField()
    reciept_no = models.IntegerField()
    reciept_student = models.ForeignKey(students,on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50)
    reciept_inv = models.ForeignKey(addindfee,on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    usr = models.ForeignKey(User,on_delete=models.CASCADE)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.reciept_student.first_name + " " + self.reciept_student.last_name


class PayUTransaction(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('success',   'Success'),
        ('failure',   'Failure'),
        ('pending',   'Pending'),
    ]
    txnid       = models.CharField(max_length=100, unique=True)
    invoice     = models.ForeignKey('addindfee', on_delete=models.CASCADE, related_name='transactions')
    student     = models.ForeignKey(students,on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    payu_txnid  = models.CharField(max_length=100, blank=True, null=True)  # PayU's own txnid
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.txnid} | {self.student} | {self.status}"

    @staticmethod
    def generate_txnid():
        return 'MITHRAN' + uuid.uuid4().hex[:10].upper()

class SchoolPayUConfig(models.Model):
    school         = models.ForeignKey(school, on_delete=models.CASCADE, related_name='payu_config')
    merchant_key   = models.CharField(max_length=100)
    merchant_salt  = models.CharField(max_length=100)
    is_active      = models.BooleanField(default=False)  # toggle online pay on/off
    is_test        = models.BooleanField(default=True)   # test vs production

    def __str__(self):
        return f"{self.school.name} - PayU Config"

    @property
    def base_url(self):
        if self.is_test:
            return 'https://test.payu.in/_payment'
        return 'https://secure.payu.in/_payment'