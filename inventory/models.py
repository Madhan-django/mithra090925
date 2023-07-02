import datetime
from setup.models import academicyr
from django.db import models
from institutions.models import school
from setup.models import sclass
from admission.models import students
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    Cat_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=35)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    contact_number2 = models.CharField(max_length=20)
    Sup_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class products(models.Model):
    name = models.CharField(max_length=100)
    sch = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    name = models.ForeignKey(products,on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    invoice_no = models.IntegerField()
    order_dt = models.DateField()
    rec_dt = models.DateField()
    Prod_school = models.ForeignKey(school,on_delete=models.CASCADE)

    @property
    def total_cost(self):
        return self.quantity * self.price



class stock(models.Model):
    name = models.ForeignKey(products,on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    Prod_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name

class Order(models.Model):
    product = models.ForeignKey(stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class product_set(models.Model):
    pclass = models.ForeignKey(sclass,on_delete=models.CASCADE)
    prod_set = models.ForeignKey(stock, on_delete=models.CASCADE)
    qty = models.IntegerField()
    ac_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)



    def __str__(self):
        return self.pclass.name

class book_set_issue(models.Model):
    book_set = models.ForeignKey(product_set,on_delete=models.CASCADE)
    issue_date = models.DateField(default=datetime.today())
    stud_class = models.ForeignKey(sclass,on_delete=models.CASCADE)
    book_student = models.ForeignKey(students,on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    set_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.book_student.first_name

class ind_book(models.Model):
    inv_prod = models.ForeignKey(products,on_delete=models.CASCADE)
    issue_date = models.DateField(default=datetime.today())
    bclass = models.ForeignKey(sclass, on_delete=models.CASCADE)
    stud = models.ForeignKey(students,on_delete=models.CASCADE)
    isbook_set = models.CharField(max_length=5)
    qty = models.IntegerField()
    status = models.CharField(max_length=10)
    ind_school = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


