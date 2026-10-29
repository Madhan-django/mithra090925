from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import school, SchoolMenuPermission, GroupMenuPermission
from authenticate.decorators import allowed_users,unauthenticated_user
from django.http import HttpResponseRedirect
from .forms import add_school

# Create your views here.

@allowed_users(allowed_roles=['superadmin'])
def selectschool(request):
    data = school.objects.all()
    user = request.user
    return render(request,'panel/admindash.html',context={'data':data,'user':user})


def allschool(request):
    request.session['sch_id'] = school_id
    sch_id = request.session['sch_id']
    data = school.objects.get(pk=school_id)
    hide = 1

    return render(request,'institutions/schoollists.html',context={'data':data})

@allowed_users(allowed_roles=['superadmin'])
def addschool(request):

    if request.method =='POST':
        form= add_school(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    form= add_school()
    return render(request,'institutions/addschool.html',context={'form':form})

@allowed_users(allowed_roles=['superadmin'])
def schoollist(request,school_id):
    request.session['sch_id'] = school_id
    sch_id = request.session['sch_id']
    data = school.objects.get(pk=school_id)
    return redirect('home_dashboard')

@allowed_users(allowed_roles=['superadmin'])
def delschool(request,school_id):
    fm = school.objects.get(pk=school_id)
    fm.delete()
    messages.success(request,'Institution Deleted Successfully')
    return HttpResponseRedirect('institutions')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updateschool(request, sch_id):
    # Get school instance from session
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)

    print("=== BEFORE FORM INIT ===")
    for field in sdata._meta.fields:
        print(f"{field.name} = {getattr(sdata, field.name)}")

    if request.method == "POST":
        form = add_school(request.POST, request.FILES, instance=sdata)
        print("=== POST DATA RECEIVED ===")
        for key, value in request.POST.items():
            print(f"{key} = {value}")
        print("FILES RECEIVED:")
        for key, value in request.FILES.items():
            print(f"{key} = {value}")

        if form.is_valid():
            form.save()
            messages.success(request, 'Institution updated successfully')
            return redirect('institutions')
        else:
            print("=== FORM ERRORS ===")
            for field, errors in form.errors.items():
                print(f"{field} errors: {errors}")

    # Initialize form for GET or after invalid POST
    form = add_school(instance=sdata)

    print("=== AFTER FORM INIT ===")
    for field in form.fields:
        print(f"{field} = {form[field].value()}")

    return render(request, 'institutions/updateschool.html', {'form': form})



@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def conf_school(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = school.objects.get(pk=sch_id)
    return render(request,'institutions/school.html',context={'sch':data,'skool':sdata})


MENU_MODULES = [
    ('admission',     'Admission',     'ri-sticky-note-line'),
    ('students',      'Students',      'ri-team-line'),
    ('staffs',        'Staffs',        'ri-group-line'),
    ('academics',     'Academics',     'ri-award-line'),
    ('timetable',     'Timetable',     'ri-calendar-schedule-line'),
    ('finance',       'Finance',       'ri-coins-line'),
    ('payroll',       'Payroll',       'ri-bank-card-line'),
    ('petty_cash',    'Petty Cash',    'ri-cash-line'),
    ('transport',     'Transport',     'ri-bus-line'),
    ('hostel',        'Hostel',        'ri-building-2-line'),
    ('examination',   'Examination',   'ri-task-line'),
    ('question_bank', 'Question Bank', 'ri-question-answer-line'),
    ('library',       'Library',       'ri-book-shelf-line'),
    ('assets',        'Assets',        'ri-server-line'),
    ('inventory',     'Inventory',     'ri-shopping-cart-2-line'),
    ('visitors',      'Visitors',      'ri-pass-valid-line'),
    ('reports',       'Reports',       'ri-file-chart-line'),
    ('jacob_reports', 'Jacob Reports', 'ri-file-list-3-line'),
    ('certificates',  'Certificates',  'ri-medal-line'),
]


@allowed_users(allowed_roles=['superadmin'])
def manage_menu_permissions(request, school_id):
    sch = get_object_or_404(school, pk=school_id)
    perm, _ = SchoolMenuPermission.objects.get_or_create(school=sch)

    if request.method == 'POST':
        for field, _, _ in MENU_MODULES:
            setattr(perm, field, field in request.POST)
        perm.save()
        messages.success(request, f'Menu permissions updated for {sch.name}')
        return redirect('manage_menu_permissions', school_id=school_id)

    modules_with_values = [
        {'field': field, 'label': label, 'icon': icon, 'enabled': getattr(perm, field)}
        for field, label, icon in MENU_MODULES
    ]

    return render(request, 'institutions/menu_permissions.html', {
        'sch': sch,
        'modules_with_values': modules_with_values,
    })


@allowed_users(allowed_roles=['superadmin'])
def menu_permissions_current(request):
    sch_id = request.session.get('sch_id')
    if sch_id:
        return redirect('manage_menu_permissions', school_id=sch_id)
    return redirect('select')


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def group_permissions_current(request):
    sch_id = request.session.get('sch_id')
    if sch_id:
        return redirect('group_permissions_list', school_id=sch_id)
    return redirect('select')


GROUP_MENU_MODULES = [
    # (field_name, label, section)
    ('admission',            'Admission',              'Modules'),
    ('students',             'Students',               'Modules'),
    ('staffs',               'Staffs',                 'Modules'),
    ('academics',            'Academics',              'Modules'),
    ('timetable',            'Timetable',              'Modules'),
    ('finance',              'Finance',                'Modules'),
    ('payroll',              'Payroll',                'Modules'),
    ('transport',            'Transport',              'Modules'),
    ('hostel',               'Hostel',                 'Modules'),
    ('petty_cash',           'Petty Cash',             'Modules'),
    ('examination',          'Examination',            'Modules'),
    ('question_bank',        'Question Bank',          'Modules'),
    ('library',              'Library',                'Modules'),
    ('assets',               'Assets',                 'Modules'),
    ('inventory',            'Inventory',              'Modules'),
    ('visitors',             'Visitors',               'Modules'),
    ('reports',              'Reports',                'Modules'),
    ('jacob_reports',        'Jacob Reports',          'Modules'),
    ('certificates',         'Certificates',           'Modules'),
    ('configurations',       'Configurations/Settings','Admin Features'),
    ('students_authenticate','Student Auth Mgmt',      'Admin Features'),
    ('students_promote',     'Student Promotion',      'Admin Features'),
    ('students_transfer',    'Student Transfer',       'Admin Features'),
]


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def group_permissions_list(request, school_id):
    sch = get_object_or_404(school, pk=school_id)
    groups = Group.objects.all()
    existing = {
        p.group_id: p
        for p in GroupMenuPermission.objects.filter(school=sch)
    }
    group_rows = [
        {'group': g, 'perm': existing.get(g.id)}
        for g in groups
    ]
    return render(request, 'institutions/group_permissions_list.html', {
        'sch': sch,
        'group_rows': group_rows,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def manage_group_permissions(request, school_id, group_id):
    sch   = get_object_or_404(school, pk=school_id)
    grp   = get_object_or_404(Group, pk=group_id)
    perm, _ = GroupMenuPermission.objects.get_or_create(group=grp, school=sch)

    if request.method == 'POST':
        for field, _, _ in GROUP_MENU_MODULES:
            setattr(perm, field, field in request.POST)
        perm.save()
        messages.success(request, f'Permissions updated for "{grp.name}" in {sch.name}')
        return redirect('manage_group_permissions', school_id=school_id, group_id=group_id)

    modules = [
        {'field': field, 'label': label, 'section': section, 'enabled': getattr(perm, field)}
        for field, label, section in GROUP_MENU_MODULES
    ]

    return render(request, 'institutions/group_permissions.html', {
        'sch': sch,
        'group': grp,
        'modules': modules,
    })
