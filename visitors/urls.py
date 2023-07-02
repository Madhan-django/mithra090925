from django.urls import path
from . import views

urlpatterns = [
    path('visitors_list',views.visitors_list,name='visitors_list'),
    path('add_visitor',views.add_visitor,name='add_visitor'),
    path('update_visitor/<visitor_id>',views.update_visitor,name='update_visitor'),
    path('delete_visitor/<visitor_id>',views.delete_visitor,name='delete_visitor'),
    path('view_visitor/<visit_id>',views.view_visitor,name='view_visitor'),

]

