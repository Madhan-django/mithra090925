from django.shortcuts import render,HttpResponse,redirect
from .models import books,library_card,book_issued
from institutions.models import school
from admission.models import students
from setup.models import academicyr,currentacademicyr,sclass,section
from authenticate.decorators import allowed_users
from .forms import add_book_form,add_bookissue_form
from django.contrib import messages
from django.db import IntegrityError
from datetime import date
from .utils import render_to_pdf


# Create your views here.

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Teacher'])
def books_list(request):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   data = books.objects.filter(book_school=sdata)
   return render(request,'library/books.html',context={'data':data,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def add_book(request):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr,school_name=sdata)
   initial_data = {
      'book_school': sdata,

   }
   if request.method == "POST":
      form = add_book_form(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,'Book Added Successfully')
         return redirect('books_list')

   form = add_book_form(initial=initial_data)
   return render(request,'library/add_book.html',context={'form':form,'skool':sdata,'year':year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def lib_card(request):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   data = library_card.objects.filter(lib_school=sdata,acad_year=yr)
   return render(request,'library/cards.html',context={'data':data,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def gen_lib_card(request):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   lib_class = sclass.objects.filter(school_name=sdata,acad_year=yr)
   data = library_card.objects.filter(lib_school=sdata)

   if request.method == 'POST':
      prefix = request.POST.get('prefix')
      starting = request.POST.get('start_no')
      cls= request.POST.get('class_name')
      cls_name = sclass.objects.get(pk=cls)
      secs = request.POST.get('secs')
      sec_name = section.objects.get(pk=secs)
      stud= students.objects.filter(ac_year=year, class_name=cls_name, secs=sec_name)
      
      for stu in stud:
         starting=str(starting)
         cardno = prefix+starting
         library_card.objects.create(card_no= cardno,issued_to=stu,acad_year=yr,card_issued_date=date.today(),lib_school=sdata)
         starting = int(starting)
         starting = starting + 1
      messages.success(request,'CARD Generated Successfully')
   return render(request, 'library/gen_lib_card.html',
                 context={'lib_class': lib_class, 'skool': sdata, 'year': year, 'data': data})




def load_section(request):
   class_id = request.GET.get('Class_Id')
   ssection = section.objects.filter(class_sec_name=class_id).order_by('class_sec_name')
   return render(request, 'library/selectsection.html', context={'ssection': ssection})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def add_book_issued(request,libbook_id):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   lib_class = sclass.objects.filter(school_name=sdata,acad_year=yr)
   bk = books.objects.get(pk=libbook_id)
   initial_data = {
      'book_title':bk,
      'acd_year':year

   }
   if request.method == 'POST':
      form = add_bookissue_form(request.POST)
      if form.is_valid():
         form.issued_quantity=1
         bk.issued = bk.issued +1
         bk.save()
         form.save()
         messages.success(request,'Book Issued Successfully')
      else:
         messages.success(request,'Validation Error')

   form = add_bookissue_form(initial=initial_data)
   return render(request,'library/book_issued.html',context={'form':form,'bk':bk,'skool':sdata,'year':year,'lib_class':lib_class})

def load_student(request):
   secsId = request.GET.get('SecsId')
   stud = students.objects.filter(secs=secsId).order_by('secs')

   return render(request, 'library/selectstudent.html', context={'stud': stud})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def issued_booklist(request):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   data = book_issued.objects.filter(book_title__book_school=sdata)
   return render(request,'library/issued.html',context={'data':data,'skool':sdata,'year':year})


@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def book_return(request,libbook_id):
   data = book_issued.objects.get(pk=libbook_id)
   data.status='Returned'
   test = data.book_title.id
   bk = books.objects.get(pk=test)
   bk.issued = bk.issued - 1
   bk.save()
   data.save()
   messages.success(request,'Book Returned Successfully')
   return redirect('issued_booklist')



@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def search_issued(request):
   sch_id = sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id )
   year = currentacademicyr.objects.get(school_name=sch_id)
   Searchby = request.POST['searchby']
   Searched = request.POST['searched']
   if Searchby == 'studname':
      data = book_issued.objects.filter(book_title__book_school=sdata, issued_to=Searched)
   elif Searchby == 'issued_date':
      data = book_issued.objects.filter(book_title__book_school=sdata, issued_date=Searched)
   elif Searchby == 'book_title':
      data = book_issued.objects.filter(book_title__book_school=sdata, book_title=Searched)
   elif Searchby == 'status':
      data = book_issued.objects.filter(book_title__book_school=sdata, status=Searched)
   else:
      data = book_issued.objects.filter(book_title__book_school=sdata, status='Issued')
   return render(request, 'library/issued.html', context={'data': data, 'skool': sdata, 'year': year})

@allowed_users(allowed_roles=['superadmin','Admin','Accounts','Librarian'])
def print_card(request,libcard_id):
   sch_id = request.session['sch_id']
   sdata = school.objects.get(pk=sch_id)
   yr = currentacademicyr.objects.get(school_name=sdata)
   year = academicyr.objects.get(acad_year=yr, school_name=sdata)
   rec_data = library_card.objects.get(pk=libcard_id)
   data = {
      'rec_data': rec_data,
      'skool': sdata,
      'year':year
   }
   pdf = render_to_pdf('library/print_card.html',data)
   return HttpResponse(pdf, content_type='application/pdf')



