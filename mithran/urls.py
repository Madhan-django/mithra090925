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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_delete_policy/', TemplateView.as_view(template_name='user_deletion_policy.html'), name='user_delete_policy'),
    path('institutions/',include('institutions.urls')),
    path('setup/',include('setup.urls')),
    path('admission/',include('admission.urls')),
    path('students/',include('students.urls')),
    path('fees/',include('fees.urls')),
    path('examination/',include('examination.urls')),
    path('library/',include('library.urls')),
    path('staff/',include('staff.urls')),
    path('',include('authenticate.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('inventory/',include('inventory.urls')),
    path('visitors/',include('visitors.urls')),
    path('studentportal/',include('studentportal.urls')),
    path('academic/',include('academic.urls')),
    path('dashboard/',include('dashboards.urls')),
    path('reports/',include('reports.urls')),
    path('studentsapi/',include('studentsapi.urls')),
    path('mobi/',include('mobi.urls')),
    path('push_messages/',include('pushnotify.urls')),
    path('mobiplayer/',include('mobiplayer.urls')),
    path('uploads/',include('uploads.urls')),
    path('digiattend/',include('digiattend.urls')),
    path('sera/',include('sera.urls')),
    path('pettycash/',include('pettycash.urls')),
    path('payroll/',include('payroll.urls')),
    path('timetable/',include('timetable.urls')),
    path('automate/',include('automate.urls')),
    path('tally/',include('tally.urls')),
    path('assets/',include('assets.urls')),
    path('grievance/',include('grievance.urls')),
    path('jacobreports/',include('jacobreports.urls')),
    path('qbank/',include('qbank.urls')),
    path('transport/', include('transport.urls')),
    path('hostel/', include('hostel.urls')),
    path('lessonplan/', include('lessonplan.urls')),
    path('certificates/', include('certificates.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
