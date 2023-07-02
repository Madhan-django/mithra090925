from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from global_login_required import login_not_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from staff.models import staff
from institutions.models import school

# Create your views here.


@login_not_required
def login_user(request):
    if request.user.is_authenticated:
        user = request.user
        usr = request.user.username
        suser = User.objects.get(username=usr)
        if user.groups.filter(name='superadmin').exists():
            request.session['visible'] = True
            return redirect('institutions')
        elif user.groups.filter(name='Admin').exists():
            data = staff.objects.get(staff_user=suser)
            sch = data.staff_school
            sdata = school.objects.get(name=sch)
            request.session['sch_id'] = sdata.id
            return redirect('conf_school')
        elif user.groups.filter(name='Teacher').exists():
            data = staff.objects.get(staff_user=suser)
            sch = data.staff_school
            sdata = school.objects.get(name=sch)
            request.session['sch_id'] = sdata.id
            return redirect('students_list')
        elif user.groups.filter(name='Accounts').exists():
            data = staff.objects.get(staff_user=suser)
            sch = data.staff_school
            sdata = school.objects.get(name=sch)
            request.session['sch_id'] = sdata.id
            return redirect('conf_school')
        else:
            print('other login success')
            return redirect('dashboard')

    if request.method == 'POST':
        usernm = request.POST.get('usernm')
        passwd = request.POST.get('passwd')
        user = authenticate(request, username=usernm, password=passwd)
        if user is not None:
            login(request, user)
            usr = request.user.username
            suser = User.objects.get(username=usr)
            if user.groups.filter(name='superadmin').exists():
                request.session['visible'] = True
                return redirect('institutions')
            elif user.groups.filter(name='Admin').exists():
                data = staff.objects.get(staff_user=suser)
                sch = data.staff_school
                sdata = school.objects.get(name=sch)
                request.session['sch_id']= sdata.id
                return redirect('conf_school')
            elif user.groups.filter(name='Teacher').exists():
                data = staff.objects.get(staff_user=suser)
                sch = data.staff_school
                sdata = school.objects.get(name=sch)
                request.session['sch_id']= sdata.id
                return redirect('students_list')
            elif user.groups.filter(name='Accounts').exists():
                data = staff.objects.get(staff_user=suser)
                sch = data.staff_school
                sdata = school.objects.get(name=sch)
                request.session['sch_id']= sdata.id
                return redirect('conf_school')
            else:
                print('other login success')
                return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password Incorrect')

    return render(request,'authenticate/authentication-login.html')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def logout_user(request):
    logout(request)
    return redirect('/')


