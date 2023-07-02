"""mithran URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework import routers
# from .views import schoolviewset,classviewset,sectionviewset,studentviewset,feesviewset,userviewset
from fees import views


#
# router = routers.DefaultRouter()
# router.register('school',schoolviewset)
# router.register('class',classviewset)
# router.register('section',sectionviewset)
# router.register('student',studentviewset)
# router.register('fees',feesviewset)
# router.register('user',userviewset)




urlpatterns = [
path('',views.fee_details,name='fee_details'),
path('fee_add',views.fee_add,name='fee_add'),
path('addindfee',views.addfeeind,name='addindfee'),
path('invoices',views.fee_invoices,name='invoices'),
path('bulkfee',views.addbulkfee,name='addbulkfee'),
path('updatefee_cat/<fee_cat_id>',views.updatefee_cat,name='updatefee_cat'),
path('delfee_cat/<fee_cat_id>',views.delfee_cat,name='delfee_cat'),
path('updateindfee/<feeind_id>',views.updateindfee,name='updateindfee'),
path('delindfee/<feeind_id>',views.delindfee,name='delindfee'),
path('addfeereciept/<feeind_id>',views.addfeereciept,name='addfeereciept'),
path('fee_reciepts',views.fee_reciepts,name='fee_reciepts'),
path('reciepts/<rec_id>',views.reprint_reciept,name='reprint_reciept'),
path('del_reciept/<rec_id>',views.del_reciept,name='del_reciept'),
path('ajax_load_class',views.load_class,name='ajax_load_class'),
path('html_to_pdf_directly/<ret_id>',views.html_to_pdf_directly,name='html_to_pdf_directly'),
path('invoice_search',views.invoice_search,name='invoice_search'),
path('invoices_download',views.invoices_download,name='invoices_download')


]
