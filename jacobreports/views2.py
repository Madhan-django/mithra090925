from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from institutions.models import school
from setup.models import academicyr,currentacademicyr,sclass
from staff.models import staff
from .models import ClassTeacherReport, InchargeReport, ClassTeacherMapping
from .forms import ClassTeacherReportForm, InchargeReportForm, ClassTeacherMappingForm


# =========================================
# REPORT LIST
# =========================================

def class_teacher_report_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    usr = request.user

    reports = ClassTeacherReport.objects.select_related(
        'school_name',
        'class_name',
        'section',
        'report_submitted_by'
    ).order_by('-report_date', '-id')

    is_admin = usr.groups.filter(name__in=['superadmin', 'Admin']).exists()

    if is_admin:
        reports = reports.filter(school_name=sdata)
    else:
        try:
            current_staff = staff.objects.get(staff_user=usr)
        except staff.DoesNotExist:
            reports = reports.none()
        else:
            mapped_teacher_ids = ClassTeacherMapping.objects.filter(
                incharge=current_staff,
                school_name=sdata
            ).values_list('class_teacher', flat=True)

            # always see own report + all mapped teachers' reports
            reports = reports.filter(
                school_name=sdata
            ).filter(
                Q(report_submitted_by=current_staff) |
                Q(report_submitted_by__in=mapped_teacher_ids)
            )

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get('search')

    if search:
        reports = reports.filter(
            Q(class_name__class_name__icontains=search) |
            Q(section__section__icontains=search) |
            Q(report_submitted_by__staff_name__icontains=search)
        )

    # =========================
    # DATE FILTER
    # =========================

    report_date = request.GET.get('report_date')

    if report_date:
        reports = reports.filter(report_date=report_date)

    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(reports, 20)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'report_date': report_date,
    }

    return render(
        request,
        'jacobreports/class_teacher_report_list.html',
        context
    )


# =========================================
# VIEW REPORT DETAIL
# =========================================

def view_class_teacher_report(request, report_id):
    report = get_object_or_404(
        ClassTeacherReport.objects.select_related(
            'school_name', 'class_name', 'section', 'report_submitted_by'
        ),
        id=report_id
    )
    return render(request, 'jacobreports/class_teacher_report_detail.html', {'report': report})


# =========================================
# ADD REPORT
# =========================================

def add_class_teacher_report(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    usr = request.user
    stf = staff.objects.get(staff_user=usr)

    # =========================
    # CLONE PREVIOUS REPORT
    # =========================

    clone_id = request.GET.get('clone')

    initial_data = {

    }

    if clone_id:

        old_report = get_object_or_404(
            ClassTeacherReport,
            id=clone_id
        )

        for field in ClassTeacherReport._meta.fields:

            if field.name not in [
                'id',
                'created_at',
                'report_date'
            ]:
                initial_data[field.name] = getattr(
                    old_report,
                    field.name
                )

        initial_data['report_date'] = date.today()

    # =========================
    # SAVE FORM
    # =========================

    if request.method == 'POST':

        form = ClassTeacherReportForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Class teacher report added successfully.'
            )

            return redirect(
                'class_teacher_report_list'
            )

    else:

        form = ClassTeacherReportForm(
            initial=initial_data
        )

        form.fields['school_name'].queryset = school.objects.filter(id=sch_id)
        form.fields['class_name'].queryset = sclass.objects.filter(school_name=sdata)
        form.fields['report_submitted_by'].queryset= staff.objects.filter(staff_user=usr)
    context = {
        'form': form
    }

    return render(
        request,
        'jacobreports/class_teacher_report_form.html',
        context
    )


# =========================================
# EDIT REPORT
# =========================================

def edit_class_teacher_report(request, report_id):

    report = get_object_or_404(
        ClassTeacherReport,
        id=report_id
    )

    if request.method == 'POST':

        form = ClassTeacherReportForm(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Report updated successfully.'
            )

            return redirect(
                'class_teacher_report_list'
            )

    else:

        form = ClassTeacherReportForm(
            instance=report
        )

    context = {
        'form': form,
        'report': report
    }

    return render(
        request,
        'jacobreports/edit_class_teacher_report.html',
        context
    )


# =========================================
# DELETE REPORT
# =========================================

def delete_class_teacher_report(request, report_id):

    report = get_object_or_404(
        ClassTeacherReport,
        id=report_id
    )

    report.delete()

    messages.success(
        request,
        'Report deleted successfully.'
    )

    return redirect(
        'class_teacher_report_list'
    )


# =========================================
# INCHARGE REPORT — LIST
# =========================================

def incharge_report_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    reports = InchargeReport.objects.filter(
        school_name=sdata
    ).select_related(
        'school_name', 'report_submitted_by'
    )

    search = request.GET.get('search', '')
    report_date = request.GET.get('report_date', '')
    department = request.GET.get('department', '')

    if search:
        reports = reports.filter(
            Q(report_submitted_by__staff_name__icontains=search) |
            Q(department__icontains=search)
        )

    if report_date:
        reports = reports.filter(report_date=report_date)

    if department:
        reports = reports.filter(department=department)

    paginator = Paginator(reports, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'search': search,
        'report_date': report_date,
        'department': department,
        'department_choices': InchargeReport.DEPARTMENT_CHOICES,
    }

    return render(request, 'jacobreports/incharge_report_list.html', context)


# =========================================
# INCHARGE REPORT — DETAIL
# =========================================

def view_incharge_report(request, report_id):
    report = get_object_or_404(
        InchargeReport.objects.select_related('school_name', 'report_submitted_by'),
        id=report_id
    )
    return render(request, 'jacobreports/incharge_report_detail.html', {'report': report})


# =========================================
# INCHARGE REPORT — ADD
# =========================================

def add_incharge_report(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    usr = request.user

    is_superadmin = usr.groups.filter(name='superadmin').exists()

    if is_superadmin:
        staff_qs = staff.objects.filter(staff_school=sdata)
    else:
        staff_qs = staff.objects.filter(staff_user=usr)

    clone_id = request.GET.get('clone')
    initial_data = {}

    if clone_id:
        old = get_object_or_404(InchargeReport, id=clone_id)
        for field in InchargeReport._meta.fields:
            if field.name not in ['id', 'created_at', 'report_date']:
                initial_data[field.name] = getattr(old, field.name)
        initial_data['report_date'] = date.today()
    elif is_superadmin:
        first_staff = staff_qs.first()
        if first_staff:
            initial_data['report_submitted_by'] = first_staff.pk

    if request.method == 'POST':
        form = InchargeReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incharge report added successfully.')
            return redirect('incharge_report_list')
    else:
        form = InchargeReportForm(initial=initial_data)
        form.fields['school_name'].queryset = school.objects.filter(id=sch_id)
        form.fields['report_submitted_by'].queryset = staff_qs

    return render(request, 'jacobreports/incharge_report_form.html', {'form': form, 'title': 'ADD INCHARGE REPORT'})


# =========================================
# INCHARGE REPORT — EDIT
# =========================================

def edit_incharge_report(request, report_id):
    report = get_object_or_404(InchargeReport, id=report_id)

    if request.method == 'POST':
        form = InchargeReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Incharge report updated successfully.')
            return redirect('incharge_report_list')
    else:
        form = InchargeReportForm(instance=report)

    return render(request, 'jacobreports/incharge_report_form.html', {
        'form': form,
        'report': report,
        'title': 'EDIT INCHARGE REPORT'
    })


# =========================================
# INCHARGE REPORT — DELETE
# =========================================

def delete_incharge_report(request, report_id):
    report = get_object_or_404(InchargeReport, id=report_id)
    report.delete()
    messages.success(request, 'Incharge report deleted successfully.')
    return redirect('incharge_report_list')


# =========================================
# CLASS TEACHER MAPPING — MANAGE
# =========================================

def manage_class_teacher_mappings(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    usr = request.user
    is_admin = usr.groups.filter(name__in=['superadmin', 'Admin']).exists()

    try:
        current_staff = staff.objects.get(staff_user=usr)
    except staff.DoesNotExist:
        current_staff = None

    staff_qs = staff.objects.filter(staff_school=sdata).order_by('first_name', 'last_name')

    if request.method == 'POST':
        form = ClassTeacherMappingForm(request.POST)
        form.fields['incharge'].queryset = staff_qs
        form.fields['class_teachers'].queryset = staff_qs
        if form.is_valid():
            incharge_staff = form.cleaned_data['incharge'] if is_admin else current_staff
            selected_teachers = form.cleaned_data['class_teachers']
            added, skipped = 0, 0
            for teacher in selected_teachers:
                _, created = ClassTeacherMapping.objects.get_or_create(
                    school_name=sdata,
                    incharge=incharge_staff,
                    class_teacher=teacher
                )
                if created:
                    added += 1
                else:
                    skipped += 1
            if added:
                messages.success(request, f'{added} mapping(s) added successfully.')
            if skipped:
                messages.warning(request, f'{skipped} mapping(s) already existed and were skipped.')
        else:
            messages.error(request, 'Please correct the errors below.')
        return redirect('manage_class_teacher_mappings')

    form = ClassTeacherMappingForm()
    form.fields['class_teachers'].queryset = staff_qs

    if is_admin:
        form.fields['incharge'].queryset = staff_qs
        mappings = ClassTeacherMapping.objects.filter(
            school_name=sdata
        ).select_related('incharge', 'class_teacher').order_by(
            'incharge__first_name', 'class_teacher__first_name'
        )
    else:
        form.fields['incharge'].queryset = staff_qs
        if current_staff:
            form.fields['incharge'].initial = current_staff.pk
        mappings = ClassTeacherMapping.objects.filter(
            school_name=sdata,
            incharge=current_staff
        ).select_related('incharge', 'class_teacher').order_by(
            'class_teacher__first_name'
        )

    context = {
        'form': form,
        'mappings': mappings,
        'is_admin': is_admin,
        'current_staff': current_staff,
    }

    return render(request, 'jacobreports/class_teacher_mappings.html', context)


# =========================================
# CLASS TEACHER MAPPING — DELETE
# =========================================

def delete_class_teacher_mapping(request, mapping_id):
    mapping = get_object_or_404(ClassTeacherMapping, id=mapping_id)
    usr = request.user
    is_admin = usr.groups.filter(name__in=['superadmin', 'Admin']).exists()

    if not is_admin:
        try:
            current_staff = staff.objects.get(staff_user=usr)
        except staff.DoesNotExist:
            messages.error(request, 'Permission denied.')
            return redirect('manage_class_teacher_mappings')
        if mapping.incharge != current_staff:
            messages.error(request, 'You can only remove your own mappings.')
            return redirect('manage_class_teacher_mappings')

    mapping.delete()
    messages.success(request, 'Mapping removed successfully.')
    return redirect('manage_class_teacher_mappings')