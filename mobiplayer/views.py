from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.utils import timezone
from institutions.models import school
from setup.models import currentacademicyr,academicyr
from .models import Video
from .forms import NewVideoForm

# Create your views here.

def listvideo(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    data = Video.objects.filter(Vschool=sdata)
    return render(request,'mobiplayer/videolist.html',context={'data':data,'skool':sdata,'year':year})

def NewVideo(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    initial_data = {
        'Vschool' : sdata,
        'Vpostdate' : timezone.now().date()
    }
    if request.method == 'POST':
        form = NewVideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Video Saved Successfully')
            return redirect('listvideo')
    form = NewVideoForm(initial=initial_data)
    return render(request,'mobiplayer/NewVideo.html',context={'form':form,'skool':sdata,'year':year})


def EditVideo(request,vid_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.filter(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    video = Video.objects.get(id=vid_id)
    if request.method == 'POST':
        form = NewVideoForm(request.POST,request.FILES,instance=video)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Updated Successfully')
    else:
        form = NewVideoForm(instance=video)
    return render(request,'mobiplayer/UpdateVideo.html',context={'form':form,'skool':sdata,'year':year})

def DeleteVideo(request,vid_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.filter(id=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    video = Video.objects.get(id=vid_id)
    video.delete()
    messages.success(request,"Record Deleted Successfully")
    return redirect('listvideo')

