from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.fee_details), name='fee_details'),
    path('fee_add/', login_required(views.fee_add), name='fee_add'),
    path('addindfee/', login_required(views.addfeeind), name='addindfee'),
    path('invoices/', login_required(views.fee_invoices), name='invoices'),
    path('bulkfee/', login_required(views.addbulkfee), name='addbulkfee'),
    path('updatefee_cat/<int:fee_cat_id>/', login_required(views.updatefee_cat), name='updatefee_cat'),
    path('delfee_cat/<int:fee_cat_id>/', login_required(views.delfee_cat), name='delfee_cat'),
    path('updateindfee/<int:feeind_id>/', login_required(views.updateindfee), name='updateindfee'),
    path('delindfee/<int:feeind_id>/', login_required(views.delindfee), name='delindfee'),
    path('addfeereciept/<int:feeind_id>/', login_required(views.addfeereciept), name='addfeereciept'),
    path('fee_reciepts/', login_required(views.fee_reciepts), name='fee_reciepts'),
    path('reciepts/<int:rec_id>/', login_required(views.reprint_reciept), name='reprint_reciept'),
    path('del_reciept/<int:rec_id>/', login_required(views.del_reciept), name='del_reciept'),
    path('ajax_load_class/', login_required(views.load_class), name='ajax_load_class'),
    path('html_to_pdf_directly/<int:ret_id>/', login_required(views.html_to_pdf_directly), name='html_to_pdf_directly'),
    path('invoice_search/', login_required(views.invoice_search), name='invoice_search'),
    path('invoices_download/', login_required(views.invoices_download), name='invoices_download'),
    path('reciept_search/', login_required(views.reciept_search), name='reciept_search'),
    path('temp_inv/', login_required(views.temp_inv), name='temp_inv'),
    path('daily_collection',login_required(views.daily_collection),name='daily_collection'),
    path('fee_invoices_del',views.fee_invoices_del,name='fee_invoices_del'),
    path('updateindfee_cat/<int:feeind_id>/', login_required(views.updateindfee_cat), name='updateindfee_cat'),
]


