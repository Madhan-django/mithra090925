from django.urls import path
from . import  views
from django.contrib.auth.decorators import login_required


urlpatterns=[
    path('',views.login_user,name='login_user'),
    path('logout/',login_required(views.logout_user),name='logout_user'),
    path('adminpanel',login_required(views.adminpanel),name='adminpanel'),
]
