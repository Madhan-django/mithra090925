from django.contrib import admin
from .models import CertificateTemplate, CertificateIssued


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display  = ['name', 'cert_type', 'school', 'is_active', 'created_at']
    list_filter   = ['cert_type', 'is_active', 'school']
    search_fields = ['name', 'school__name']


@admin.register(CertificateIssued)
class CertificateIssuedAdmin(admin.ModelAdmin):
    list_display  = ['cert_number', 'student', 'cert_type', 'issued_date', 'issued_by']
    list_filter   = ['cert_type', 'issued_date', 'school']
    search_fields = ['cert_number', 'student__first_name', 'student__last_name']
    readonly_fields = ['cert_number', 'extra_context', 'created_at']
