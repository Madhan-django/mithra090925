import re
from io import BytesIO
from datetime import date, datetime
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from institutions.models import school, GroupMenuPermission, SchoolMenuPermission
from setup.models import currentacademicyr
from admission.models import students

from .models import CertificateTemplate, CertificateIssued, CERT_TYPES


def _has_cert_permission(request):
    """Return True if the user's school and group both have certificates enabled."""
    if request.user.groups.filter(name='superadmin').exists():
        return True
    sch_id = request.session.get('sch_id')
    if not sch_id:
        return False
    try:
        if not SchoolMenuPermission.objects.get(school_id=sch_id).certificates:
            return False
    except SchoolMenuPermission.DoesNotExist:
        pass
    group = request.user.groups.first()
    if group:
        try:
            if not GroupMenuPermission.objects.get(group=group, school_id=sch_id).certificates:
                return False
        except GroupMenuPermission.DoesNotExist:
            pass
    return True


def cert_permission_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not _has_cert_permission(request):
            messages.error(request, 'You do not have permission to access Certificates.')
            return redirect('home_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# Variables that are auto-filled from student/school data
KNOWN_VARS = {
    'student_name', 'first_name', 'last_name',
    'father_name', 'mother_name', 'father_occupation', 'mother_occupation',
    'gender', 'gender_he_she', 'gender_his_her',
    'dob', 'dob_words', 'age',
    'class_name', 'section', 'class_section',
    'admission_no', 'roll_no',
    'religion', 'caste', 'blood_group', 'address',
    'academic_year',
    'school_name', 'school_address', 'school_phone', 'school_email',
    'issue_date', 'cert_number', 'tc_date',
}


def _school(request):
    return school.objects.get(pk=request.session['sch_id'])


def _dob_to_words(d):
    try:
        from num2words import num2words
        day   = num2words(d.day, to='ordinal').title()
        month = d.strftime('%B')
        year  = num2words(d.year).title()
        return f"{day} {month} {year}"
    except Exception:
        return d.strftime('%d %B %Y')


def _extract_custom_vars(docx_path):
    """Return set of {{ var }} placeholders in the DOCX that are not auto-filled."""
    try:
        from docx import Document
        doc  = Document(docx_path)
        text = ' '.join(p.text for p in doc.paragraphs)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += ' ' + cell.text
        found = set(re.findall(r'\{\{\s*(\w+)', text))
        return sorted(found - KNOWN_VARS)
    except Exception:
        return []


def _build_context(stu, sdata, issue_date, cert_number):
    try:
        acad_yr = str(currentacademicyr.objects.get(school_name=sdata).current_year.acad_year)
    except Exception:
        acad_yr = str(stu.ac_year)

    age = (issue_date - stu.dob_date).days // 365

    gender_map = {'Male': ('He', 'His'), 'Female': ('She', 'Her')}
    he_she, his_her = gender_map.get(stu.gender or '', ('They', 'Their'))

    section_name = stu.secs.section_name if stu.secs else ''

    return {
        'student_name':       f"{stu.first_name} {stu.last_name}",
        'first_name':         stu.first_name,
        'last_name':          stu.last_name,
        'father_name':        stu.father_name,
        'mother_name':        stu.mother_name,
        'father_occupation':  stu.father_occupation,
        'mother_occupation':  stu.mother_occupation,
        'gender':             stu.gender or '',
        'gender_he_she':      he_she,
        'gender_his_her':     his_her,
        'dob':                stu.dob_date.strftime('%d %B %Y'),
        'dob_words':          _dob_to_words(stu.dob_date),
        'age':                str(age),
        'class_name':         stu.class_name.name,
        'section':            section_name,
        'class_section':      f"{stu.class_name.name} – {section_name}" if section_name else stu.class_name.name,
        'admission_no':       str(stu.admn_no),
        'roll_no':            str(stu.roll_no),
        'religion':           stu.religion or '',
        'caste':              stu.caste or '',
        'blood_group':        stu.blood_group or '',
        'address':            stu.address or '',
        'academic_year':      acad_yr,
        'school_name':        sdata.name,
        'school_address':     sdata.address,
        'school_phone':       sdata.phone,
        'school_email':       sdata.email,
        'issue_date':         issue_date.strftime('%d %B %Y'),
        'cert_number':        cert_number,
        'tc_date':            stu.tc_date.strftime('%d %B %Y') if stu.tc_date else '',
    }


def _next_cert_number(sdata, issue_date):
    year  = issue_date.year
    count = CertificateIssued.objects.filter(school=sdata, issued_date__year=year).count()
    return f"CERT-{sdata.id:02d}-{year}-{count + 1:04d}"


# ─── Template management ───────────────────────────────────────────────────────

@login_required
@cert_permission_required
def template_list(request):
    sdata     = _school(request)
    templates = CertificateTemplate.objects.filter(school=sdata)
    return render(request, 'certificates/template_list.html', {
        'templates':  templates,
        'cert_types': CERT_TYPES,
        'skool':      sdata,
    })


@login_required
@cert_permission_required
def template_upload(request):
    if request.method != 'POST':
        return redirect('cert_template_list')

    sdata = _school(request)
    name       = request.POST.get('name', '').strip()
    cert_type  = request.POST.get('cert_type', 'CUSTOM')
    notes      = request.POST.get('notes', '').strip()
    docx_file  = request.FILES.get('template_file')

    if not name or not docx_file:
        messages.error(request, 'Template name and file are required.')
        return redirect('cert_template_list')

    if not docx_file.name.endswith('.docx'):
        messages.error(request, 'Only .docx files are accepted.')
        return redirect('cert_template_list')

    CertificateTemplate.objects.create(
        school=sdata,
        name=name,
        cert_type=cert_type,
        template_file=docx_file,
        notes=notes,
    )
    messages.success(request, f'Template "{name}" uploaded successfully.')
    return redirect('cert_template_list')


@login_required
@cert_permission_required
def template_delete(request, pk):
    sdata = _school(request)
    tmpl  = get_object_or_404(CertificateTemplate, pk=pk, school=sdata)
    if request.method == 'POST':
        tmpl.template_file.delete(save=False)
        tmpl.delete()
        messages.success(request, 'Template deleted.')
    return redirect('cert_template_list')


@login_required
@cert_permission_required
def template_vars(request, pk):
    """AJAX: return the custom (non-auto-filled) variables found in a template."""
    sdata       = _school(request)
    tmpl        = get_object_or_404(CertificateTemplate, pk=pk, school=sdata)
    custom_vars = _extract_custom_vars(tmpl.template_file.path)
    return JsonResponse({'custom_vars': custom_vars, 'cert_type': tmpl.cert_type})


# ─── Certificate generation ────────────────────────────────────────────────────

@login_required
@cert_permission_required
def generate_cert(request):
    sdata = _school(request)

    if request.method == 'POST':
        tmpl_id    = request.POST.get('template_id')
        student_id = request.POST.get('student_id')
        issue_str  = request.POST.get('issue_date') or str(date.today())

        if not tmpl_id or not student_id:
            messages.error(request, 'Please select a template and a student.')
            return redirect('cert_generate')

        tmpl  = get_object_or_404(CertificateTemplate, pk=tmpl_id, school=sdata)
        stu   = get_object_or_404(students, pk=student_id, school_student=sdata)
        issue_date = datetime.strptime(issue_str, '%Y-%m-%d').date()

        cert_number = _next_cert_number(sdata, issue_date)
        context     = _build_context(stu, sdata, issue_date, cert_number)

        # Merge custom vars from form (prefixed with 'extra_')
        extra = {}
        for key, val in request.POST.items():
            if key.startswith('extra_') and val.strip():
                var_name          = key[len('extra_'):]
                context[var_name] = val.strip()
                extra[var_name]   = val.strip()

        try:
            from docxtpl import DocxTemplate
            doc = DocxTemplate(tmpl.template_file.path)
            doc.render(context)
        except Exception as e:
            messages.error(request, f'Error rendering template: {e}')
            return redirect('cert_generate')

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        CertificateIssued.objects.create(
            school=sdata,
            student=stu,
            template=tmpl,
            cert_number=cert_number,
            cert_type=tmpl.cert_type,
            issued_date=issue_date,
            issued_by=request.user,
            extra_context=extra,
        )

        filename = f"{cert_number}_{stu.first_name}_{stu.last_name}.docx"
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    # GET
    templates    = CertificateTemplate.objects.filter(school=sdata, is_active=True)
    all_students = students.objects.filter(school_student=sdata).order_by('first_name', 'last_name')
    return render(request, 'certificates/generate.html', {
        'templates':    templates,
        'all_students': all_students,
        'skool':        sdata,
        'today':        date.today().strftime('%Y-%m-%d'),
        'known_vars':   sorted(KNOWN_VARS),
    })


# ─── Issued list & re-download ─────────────────────────────────────────────────

@login_required
@cert_permission_required
def issued_list(request):
    sdata   = _school(request)
    qs      = CertificateIssued.objects.filter(school=sdata).select_related('student', 'template', 'issued_by')

    cert_type = request.GET.get('cert_type')
    q         = request.GET.get('q', '').strip()
    if cert_type:
        qs = qs.filter(cert_type=cert_type)
    if q:
        qs = qs.filter(
            student__first_name__icontains=q
        ) | qs.filter(student__last_name__icontains=q) | qs.filter(cert_number__icontains=q)

    return render(request, 'certificates/issued_list.html', {
        'issued':     qs[:200],
        'cert_types': CERT_TYPES,
        'skool':      sdata,
        'q':          q,
        'selected_type': cert_type,
    })


@login_required
@cert_permission_required
def redownload_cert(request, pk):
    sdata  = _school(request)
    record = get_object_or_404(CertificateIssued, pk=pk, school=sdata)

    if not record.template or not record.template.template_file:
        messages.error(request, 'Original template file no longer available.')
        return redirect('cert_issued_list')

    stu        = record.student
    issue_date = record.issued_date
    context    = _build_context(stu, sdata, issue_date, record.cert_number)
    context.update(record.extra_context)

    try:
        from docxtpl import DocxTemplate
        doc = DocxTemplate(record.template.template_file.path)
        doc.render(context)
    except Exception as e:
        messages.error(request, f'Error regenerating certificate: {e}')
        return redirect('cert_issued_list')

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    filename = f"{record.cert_number}_{stu.first_name}_{stu.last_name}.docx"
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
