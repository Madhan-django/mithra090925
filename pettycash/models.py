from django.db import models
from django.contrib.auth.models import User
from institutions.models import school
from setup.models import academicyr,currentacademicyr

class CashSource(models.Model):
    """Represents sources of petty cash (e.g., cash deposit, fund allocation)"""
    source_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    school_year = models.ForeignKey(academicyr,on_delete=models.CASCADE)
    source_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source_name} - ₹{self.amount} on {self.date_received}"


class ExpenseCategory(models.Model):
    """Optional categories: Stationery, Snacks, Transport, etc."""
    name = models.CharField(max_length=100)
    expense_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PettyCashExpense(models.Model):
    expense_no = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date_spent = models.DateField()
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    spent_by = models.CharField(max_length=55)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_by_user")
    remarks = models.TextField(blank=True)
    school_year = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    petty_school = models.ForeignKey(school, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - ₹{self.amount} on {self.date_spent}"


class PettyCashBalance(models.Model):
    """Optional: Keeps track of available cash balance"""
    date = models.DateField()
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    school_year = models.ForeignKey(academicyr, on_delete=models.CASCADE)
    balance_school = models.ForeignKey(school,on_delete=models.CASCADE)

    def __str__(self):
        return f"Balance on {self.date}: ₹{self.closing_balance}"
