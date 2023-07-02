from django.urls import path,include,re_path
from admission import views

urlpatterns = [
path('enquiry_list',views.enquiry_list,name='enquiry_list'),
path('add_enquiry',views.add_enquiry,name='add_enquiry'),
path('del_enquiry/<enq_id>',views.del_enquiry,name='del_enquiry'),
path('update_enquiry/<enq_id>',views.update_enquiry,name='update_enquiry'),
path('followup_enquiry',views.followup_enquiry,name='followup_enquiry'),
path('search_enquiry',views.search_enquiry,name='search_enquiry'),
path('addstud',views.addstudents,name='addstudents'),
path('ajax_load_section',views.load_section,name='ajax_load_section'),



    ]