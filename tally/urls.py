from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('tallyIntApi/',login_required(views.receive_tally_data),name='tallyIntApi'),



]

