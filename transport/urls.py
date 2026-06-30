from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('',                          login_required(views.transport_dashboard),  name='transport_dashboard'),

    # Vehicle types
    path('vehicle-types/',            login_required(views.vehicle_type_list),    name='vehicle_type_list'),
    path('vehicle-types/delete/<int:pk>/', login_required(views.vehicle_type_delete), name='vehicle_type_delete'),

    # Vehicles
    path('vehicles/',                 login_required(views.vehicle_list),         name='vehicle_list'),
    path('vehicles/add/',             login_required(views.vehicle_add),          name='vehicle_add'),
    path('vehicles/<int:pk>/edit/',   login_required(views.vehicle_edit),         name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', login_required(views.vehicle_delete),       name='vehicle_delete'),

    # Drivers
    path('drivers/',                  login_required(views.driver_list),          name='driver_list'),
    path('drivers/add/',              login_required(views.driver_add),           name='driver_add'),
    path('drivers/<int:pk>/edit/',    login_required(views.driver_edit),          name='driver_edit'),
    path('drivers/<int:pk>/delete/',  login_required(views.driver_delete),        name='driver_delete'),

    # Routes
    path('routes/',                   login_required(views.route_list),           name='route_list'),
    path('routes/add/',               login_required(views.route_add),            name='route_add'),
    path('routes/<int:pk>/edit/',     login_required(views.route_edit),           name='route_edit'),
    path('routes/<int:pk>/delete/',   login_required(views.route_delete),         name='route_delete'),

    # Stops
    path('routes/<int:route_pk>/stops/',         login_required(views.stop_list),   name='stop_list'),
    path('routes/<int:route_pk>/stops/add/',     login_required(views.stop_add),    name='stop_add'),
    path('stops/<int:pk>/edit/',                 login_required(views.stop_edit),   name='stop_edit'),
    path('stops/<int:pk>/delete/',               login_required(views.stop_delete), name='stop_delete'),

    # Student Allocation
    path('allocations/',              login_required(views.allocation_list),      name='allocation_list'),
    path('allocations/add/',          login_required(views.allocation_add),       name='allocation_add'),
    path('allocations/<int:pk>/edit/',   login_required(views.allocation_edit),   name='allocation_edit'),
    path('allocations/<int:pk>/delete/', login_required(views.allocation_delete), name='allocation_delete'),

    # AJAX
    path('ajax/stops/',               views.stops_for_route,                      name='stops_for_route'),

    # GPS
    path('gps/push/',                 views.gps_push,                             name='gps_push'),
    path('gps/positions/',            login_required(views.gps_positions),        name='gps_positions'),
    path('gps/live-map/',             login_required(views.live_map),             name='live_map'),
    path('gps/settings/',             login_required(views.gps_settings),         name='gps_settings'),
]
