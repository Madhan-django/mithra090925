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
                return redirect('home_dashboard')
            elif user.groups.filter(name='Teacher').exists():
                data = staff.objects.get(staff_user=suser)
                sch = data.staff_school
                sdata = school.objects.get(name=sch)
                request.session['sch_id']= sdata.id
                return redirect('home_dashboard')
            elif user.groups.filter(name='Accounts').exists():
                data = staff.objects.get(staff_user=suser)
                sch = data.staff_school
                sdata = school.objects.get(name=sch)
                request.session['sch_id']= sdata.id
                return redirect('home_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.info(request, 'Username OR Password Incorrect')

    return render(request,'authenticate/login.html')


def register_user(request):
    form = CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'adminpanel/authentication-register.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

def adminpanel(request):
    return render(request,'panel/index.html')

def Googleverify(request):
    return render(request,'GoogleVerify/googledf18bd0e30039b75.html')