from django.contrib import admin
from .models import fees,addindfee,bulkfee,fee_reciept

# Register your models here.
admin.site.register(fees)
admin.site.register(addindfee)
admin.site.register(bulkfee)
admin.site.register(fee_reciept)
