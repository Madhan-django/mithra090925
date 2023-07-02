from django.shortcuts import render,redirect
from django.contrib import messages
from .models import school
from authenticate.decorators import allowed_users,unauthenticated_user
from django.http import HttpResponseRedirect
from .forms import add_school

# Create your views here.

@allowed_users(allowed_roles=['superadmin'])
def selectschool(request):
    data = school.objects.all()
    user = request.user
    return render(request,'institutions/index.html',context={'data':data})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
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
    return render(request,'institutions/school.html',context={'sch':data})

@allowed_users(allowed_roles=['superadmin'])
def delschool(request,school_id):

    fm = school.objects.get(pk=school_id)
    fm.delete()
    messages.success(request,'Institution Deleted Successfully')
    return HttpResponseRedirect('institutions')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def updateschool(request, sch_id):
    data = school.objects.only('logo').get(pk=sch_id)
    if request.method == "POST":
        form = add_school(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Institution updated successfully')
            return redirect('institutions')
    else:
        form = add_school(instance=data)
    return render(request, 'institutions/updateschool.html', {'form': form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts'])
def conf_school(request):
    sch_id = request.session['sch_id']
    data = school.objects.get(pk=sch_id)
    return render(request,'institutions/school.html',context={'sch':data})