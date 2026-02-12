from django.db import models
from institutions.models import school
from setup.models import currentacademicyr,sclass,section,academicyr
from admission.models import students



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
