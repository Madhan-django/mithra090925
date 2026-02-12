# automate/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('fee_automate_list', login_required(views.fee_automate_list), name='fee_automate_list'),
    path('',login_required(views.automate_list),name='automate_list'),
    path('add', views.add_automate_task, name='add_automate_task'),
    path('delete/<int:task_id>',views.delete_automate_task,name='delete_automated_task')


]











