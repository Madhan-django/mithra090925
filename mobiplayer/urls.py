from django.urls import path
from . import views

urlpatterns = [
    path('listvideo',views.listvideo,name='listvideo'),
    path('NewVideo',views.NewVideo,name='NewVideo'),
    path('EditVideo/<vid_id>',views.EditVideo,name='EditVideo'),
    path('DeleteVideo/<vid_id>',views.DeleteVideo,name='DeleteVideo'),
]
