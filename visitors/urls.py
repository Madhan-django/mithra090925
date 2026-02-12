from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('visitors_list', login_required(views.visitors_list), name='visitors_list'),
    path('add_visitor', login_required(views.add_visitor), name='add_visitor'),
    path('update_visitor/<visitor_id>', login_required(views.update_visitor), name='update_visitor'),
    path('delete_visitor/<visitor_id>', login_required(views.delete_visitor), name='delete_visitor'),
    path('view_visitor/<visit_id>', login_required(views.view_visitor), name='view_visitor'),
    path('visitors_search', login_required(views.visitors_search), name='visitors_search'),
]
