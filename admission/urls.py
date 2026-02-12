from django.urls import path,include,re_path
from django.contrib.auth.decorators import login_required
from admission import views

urlpatterns = [
    path('enquiry_list/', login_required(views.enquiry_list), name='enquiry_list'),
    path('add_enquiry/', login_required(views.add_enquiry), name='add_enquiry'),
    path('del_enquiry/<int:enq_id>/', login_required(views.del_enquiry), name='del_enquiry'),
    path('update_enquiry/<int:enq_id>/', login_required(views.update_enquiry), name='update_enquiry'),
    path('followup_enquiry/', login_required(views.followup_enquiry), name='followup_enquiry'),
    path('search_enquiry/', login_required(views.search_enquiry), name='search_enquiry'),
    path('addstud/', login_required(views.addstudents), name='addstudents'),
    path('ajax_load_section/', login_required(views.load_section), name='ajax_load_section'),

]
