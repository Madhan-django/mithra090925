from django.contrib import admin
from .models import fees, addindfee, bulkfee, fee_reciept,SchoolPayUConfig,del_fee_reciept

class AddIndFeeAdmin(admin.ModelAdmin):
    search_fields = [
        'stud_name__first_name',
        'fee_cat__invoice_title',
        'status',
        '=invoice_no',
    ]
    list_display = [
        'invoice_no',
        'stud_name',
        'fee_cat',
        'class_name',
        'due_amt',
        'concession',
        'concession_apply',
        'status',
    ]
    list_filter = ['status', 'concession_apply']
    list_select_related = ['stud_name', 'fee_cat', 'class_name']
    list_per_page = 25  # limit rows per page
    ordering = ['-invoice_no']

admin.site.register(addindfee, AddIndFeeAdmin)
admin.site.register(fees)
admin.site.register(bulkfee)
admin.site.register(fee_reciept)
admin.site.register(SchoolPayUConfig)
admin.site.register(del_fee_reciept)