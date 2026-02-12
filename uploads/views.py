from django.shortcuts import render,HttpResponse,redirect
from .models import Document
from .forms import DocumentForm

# Create your views here.
def fileuploads(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('upload success')
    else:
        form = DocumentForm()
    return render(request, 'uploads/upload.html', {'form': form})

