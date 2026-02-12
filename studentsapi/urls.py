from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('posts', login_required(views.studentsapi_home), name='studentsapi_home'),
]
