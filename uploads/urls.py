from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', login_required(views.fileuploads), name='uploads'),
    ] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
