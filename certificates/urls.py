from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.template_list,   name='cert_template_list'),
    path('upload/',                       views.template_upload, name='cert_template_upload'),
    path('template/<int:pk>/delete/',     views.template_delete, name='cert_template_delete'),
    path('template/<int:pk>/vars/',       views.template_vars,   name='cert_template_vars'),
    path('generate/',                     views.generate_cert,   name='cert_generate'),
    path('issued/',                       views.issued_list,     name='cert_issued_list'),
    path('issued/<int:pk>/download/',     views.redownload_cert, name='cert_redownload'),
]
