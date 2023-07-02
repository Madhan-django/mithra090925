from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator
from admission.models import students
from institutions.models import school
from setup.models import sclass,section,currentacademicyr,academicyr
from .forms import addattendanceform,attendancegen,attendanceview
from admission.forms import add_studentsForm,trans_students
from django.contrib import messages
from authenticate.decorators import allowed_users
from .models import attendance
from .utils import render_to_pdf
import csv



# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def students_list(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year,school_name=sdata)
    data = students.objects.filter(school_student=sdata,ac_year=ayear,student_status='Active')
    paginator = Paginator(data, 30)  # Show 30 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the corresponding page object
    return render(request, 'students/sstudents.html', context={'data': page_obj, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def delstud(request,stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = students.objects.get(pk=stud_id)
    duser = User.objects.get(username=data.usernm)
    duser.delete()
    data.delete()
    messages.success(request,'Record Deleted Successfully')
    return redirect('students_list')

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def updatestud(request,stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    cdata = sclass.objects.filter(school_name=sdata).values()
    year = currentacademicyr.objects.get(school_name=sch_id)
    yr = academicyr.objects.get(school_name=sch_id, acad_year=year)
    data = students.objects.get(pk=stud_id)
    if request.method=='POST':
        form = add_studentsForm(request.POST,request.FILES,instance=data,)
        if form.is_valid():
            ussr = form.cleaned_data['usernm']
            eml = form.cleaned_data['email']
            if not User.objects.filter(username=ussr).exists():
                tmp = User.objects.create(username=ussr, email=eml, password='welcome@123')
                grp = Group.objects.get(name='student')
                tmp.groups.add(grp)

            form.save()
            messages.success(request,'Student updated successfully')
            return redirect('students_list')
    else:
        form = add_studentsForm(instance=data)

    return render(request, 'students/updatestudent.html', context={'form': form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def addattendance(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data =''
    if request.method == 'POST':
        form = attendancegen(request.POST)
        if form.is_valid():
            global glob_aclass
            global glob_asec
            global glob_attndate
            glob_aclass=form.cleaned_data['aclass']
            glob_asec = form.cleaned_data['sec']
            glob_attndate = form.cleaned_data['attndate']
            form.save()
            studen = students.objects.filter(class_name=glob_aclass, secs=glob_asec)
            for stud in studen:
                attendance.objects.create(aclass=glob_aclass, sec=glob_asec, attndate=glob_attndate,
                                          student_name=stud, status='Present')
            data = attendance.objects.filter(aclass=glob_aclass, sec=glob_asec, attndate=glob_attndate)
        else:
            messages.success(request,'Attendance Already Marked')
    form = attendancegen()
    return render(request,'attendance/addattendance.html',context={'form':form,'skool':sdata,'data':data,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def markabsent(request,stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = attendance.objects.get(pk=stud_id)
    data.status = 'Absent'
    data.save()
    messages.success(request, 'record updated Successfully')

    data = attendance.objects.filter(aclass=glob_aclass,sec=glob_asec,attndate=glob_attndate)

    form = attendancegen()
    return render(request, 'attendance/addattendance.html', context={'form': form, 'skool': sdata, 'data': data})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def markholiday(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = attendance.objects.filter(aclass=glob_aclass,sec=glob_asec,attndate=glob_attndate)

    for student in data:
        student.status = 'Holiday'
        student.save()
    data = attendance.objects.filter(aclass=glob_aclass, sec=glob_asec, attndate=glob_attndate)
    form = attendancegen()
    return render(request,'attendance/viewattendance.html', context={'form': form, 'skool': sdata, 'data': data})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def markpresent(request,stud_id):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = attendance.objects.get(pk=stud_id)
    data.status = 'Present'
    data.save()
    messages.success(request, 'record updated Successfully')

    data = attendance.objects.filter(aclass=glob_aclass,sec=glob_asec,attndate=glob_attndate)

    form = attendancegen()
    return render(request, 'attendance/addattendance.html', context={'form': form, 'skool': sdata, 'data': data})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def markallpresent(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    data = attendance.objects.filter(aclass=glob_aclass, sec=glob_asec, attndate=glob_attndate)

    for student in data:
        student.status = 'Present'
        student.save()
    data = attendance.objects.filter(aclass=glob_aclass, sec=glob_asec, attndate=glob_attndate)
    form = attendancegen()
    return render(request, 'attendance/viewattendance.html', context={'form': form, 'skool': sdata, 'data': data})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def viewattendance(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    data = ''
    global glob_aclass
    global glob_asec
    global glob_attndate
    if request.method == 'POST':
        form = attendanceview(request.POST)
        if form.is_valid():
            glob_aclass = form.cleaned_data['aclass']
            glob_asec = form.cleaned_data['sec']
            glob_attndate = form.cleaned_data['attndate']
            data = attendance.objects.filter(aclass=glob_aclass, sec=glob_asec,attndate=glob_attndate)
            print(data)
    form = attendanceview()
    return render(request, 'attendance/viewattendance.html', context={'form': form, 'skool': sdata, 'data': data,'year':year})

def load_section(request):
    class_id = request.GET.get('Class_Id')
    ssection = section.objects.filter(class_sec_name=class_id).order_by('class_sec_name')
    return render(request, 'students/selectsection.html',context={'ssection': ssection})

@allowed_users(allowed_roles=['superadmin','Admin'])
def students_promote(request):
    sch_id =   sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    cls = sclass.objects.filter(school_name=sch_id)
    sec = section.objects.filter(school_name=sch_id)
    ayear = currentacademicyr.objects.get(school_name=sch_id)
    year = academicyr.objects.get(acad_year=ayear,school_name=sdata)
    year2 = academicyr.objects.filter(school_name=sch_id)
    if request.method == 'POST':
        currclass = request.POST['classname1']
        currsec = request.POST['secsname1']
        proclass = request.POST['classname2']
        prosecs = request.POST['secsname2']
        proyear = request.POST['acadyear2']
        procls = sclass.objects.get(id=proclass)
        prosection = section.objects.get(id=prosecs)
        proyear = academicyr.objects.get(id=proyear)

        data =students.objects.filter(school_student=sch_id,class_name=currclass,secs=currsec)
        for stud in data:
            stud.ac_year=proyear
            stud.class_name=procls
            stud.secs=prosection
            stud.save()
        messages.success(request,'Students Promoted Successfully')
    return render(request,'students/students_promote.html',context={'sdata':sdata,'cls':cls,'year':year,'year2':year2})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def students_search(request):
    sch_id = sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    Searchby = request.POST['searchby']
    Searched = request.POST['searched']
    if Searchby == 'studname':
        data = students.objects.filter(first_name__startswith=Searched)
    elif Searchby == 'fathername':
        data = students.objects.filter(father_name__startswith = Searched)
    elif Searchby == 'studmob':
        data = students.objects.filter(phone__startswith = Searched)
    elif Searchby == 'studclass':
        data = students.objects.filter(class_name=Searched)
    else:
        data=students.objects.filter(student_status=Searched)
    return render(request,'students/sstudents.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def student_transfer(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    year = currentacademicyr.objects.get(school_name=sch_id)
    ayear = academicyr.objects.get(acad_year=year,school_name=sdata)
    data = students.objects.filter(school_student=sdata, ac_year=ayear, student_status='Transfer')
    return render(request, 'students/transfer.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin'])
def transfer_update(request,stud_id):
    data = students.objects.get(pk=stud_id)
    sch_add= school.objects.get(name=data.school_student)
    form = trans_students(request.POST or None,instance=data,)
    if form.is_valid():
        form.save()
        return render(request,'students/transfer_certificate.html',context={'form':data,'addr':sch_add})
    return render(request, 'students/updatetransfer.html', context={'form': form})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def print_students(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    rec_data = students.objects.filter(school_student=sdata,ac_year=year)
    data={
        'rec_data':rec_data,
        'sch_name':sdata
    }

    pdf = render_to_pdf('students/student_print.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def student_csv(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow( [sdata,])
    writer.writerow(['First Name','Last_name','Gender','DOB','Admn No','Roll No','Class','Section','Admn Date','Phone','Email','Address','Religion','Caste','Blood Group','Father Name'
                     'Mother Name','Father Occupation','Mother Occupation''Academic Year',])
    stud_data= students.objects.filter(school_student=sdata,ac_year=year)
    for obj in stud_data:
        writer.writerow([obj.first_name,obj.last_name,obj.gender,obj.dob_date, obj.admn_no,obj.roll_no,obj.class_name,obj.secs,obj.admn_date,
                         obj.phone,obj.email,obj.address,obj.religion,obj.caste,obj. blood_group,
                         obj.father_name,obj.mother_name,obj.father_occupation,obj.mother_occupation,
                         obj.ac_year,])

    return response



@allowed_users(allowed_roles=['superadmin','Admin'])
def stud_import_csv(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('import_csv')  # Redirect to the import page

        # Read the CSV file
        csv_data = csv.reader(csv_file)

        # Process the CSV data and create students objects
        for row in csv_data:
            # Create a new students object and set its attributes from CSV data
            student = students()
            student.first_name = row[0]
            student.last_name = row[1]
            student.gender = row[2]
            student.dob_date = row[3]
            student.phone = row[4]
            student.email = row[5]
            student.address = row[6]
            student.admn_no = row[7]
            student.admn_date = row[8]
            student.religion = row[9]
            student.caste = row[10]
            student.blood_group = row[11]
            student.father_name = row[12]
            student.mother_name = row[13]
            student.father_occupation = row[14]
            student.mother_occupation = row[15]
            student.roll_no = row[16]

            # Get the associated objects for foreign key fields
            ac_year = academicyr.objects.get(acad_year=row[17])
            student.ac_year = ac_year
            class_name = sclass.objects.get(class_name=row[18])
            student.class_name = class_name
            secs = section.objects.get(section_name=row[19])
            student.secs = secs
            school_student = sdata
            student.school_student = school_student

            # Set additional fields
            student.student_status = 'active'

            # Save the student object
            student.save()
        # Redirect to a success page or do something else
        return redirect('success')
    return render(request,'admission/import_csv.html',context={'skool':sdata,'year':year})




@allowed_users(allowed_roles=['superadmin','Admin'])
def download_csv_template(request):
    sch_id = request.session['sch_id']
    sdata = school.objects.get(pk=sch_id)
    yr = currentacademicyr.objects.get(school_name=sdata)
    year = academicyr.objects.get(acad_year=yr, school_name=sdata)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_template.csv"'

    writer = csv.writer(response)

    # Write the column headers
    writer.writerow([
        'First Name',
        'Last Name',
        'Gender',
        'Date of Birth',
        'Phone',
        'Email',
        'Address',
        'Admission Number',
        'Admission Date',
        'Religion',
        'Caste',
        'Blood Group',
        'Father\'s Name',
        'Mother\'s Name',
        'Father\'s Occupation',
        'Mother\'s Occupation',
        'Roll Number',
        'Academic Year',
        'Class Name',
        'Section',
        'School',
        'usernm',
    ])

    return response

