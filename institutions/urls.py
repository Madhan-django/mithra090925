from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from institutions import views

urlpatterns = [
    path('', login_required(views.selectschool), name='select'),
    path('', login_required(views.allschool), name='institutions'),
    path('addschool', login_required(views.addschool), name='addschool'),
    path('sels/<school_id>', login_required(views.schoollist), name='sels'),
    path('updateschool/<sch_id>', login_required(views.updateschool), name='updateschool'),
    path('delschool/<school_id>', login_required(views.delschool), name='delschool'),
    path('conf_school', login_required(views.conf_school), name='conf_school'),
    path('menu-permissions/<int:school_id>/', login_required(views.manage_menu_permissions), name='manage_menu_permissions'),
    path('menu-permissions/', login_required(views.menu_permissions_current), name='menu_permissions_current'),
    path('group-permissions/', login_required(views.group_permissions_current), name='group_permissions_current'),
    path('group-permissions/<int:school_id>/', login_required(views.group_permissions_list), name='group_permissions_list'),
    path('group-permissions/<int:school_id>/<int:group_id>/', login_required(views.manage_group_permissions), name='manage_group_permissions'),
]
