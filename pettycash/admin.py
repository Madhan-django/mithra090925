from django.contrib import admin
from .models import CashSource,PettyCashBalance,PettyCashExpense,ExpenseCategory

# Register your models here.
admin.site.register(CashSource)
admin.site.register(PettyCashExpense)
admin.site.register(PettyCashBalance)
admin.site.register(ExpenseCategory)