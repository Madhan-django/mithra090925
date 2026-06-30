import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, timedelta

from institutions.models import school
from setup.models import currentacademicyr, academicyr
from authenticate.decorators import allowed_users

from .models import (VehicleType, Vehicle, Driver, Route, Stop, StudentTransport,
                     GpsSettings, VehiclePosition, VehiclePositionHistory,
                     BoardingAttendance)
from .forms import VehicleTypeForm, VehicleForm, DriverForm, RouteForm, StopForm, StudentTransportForm


def _base(request):
    sch_id = request.session.get('sch_id')
    sdata  = get_object_or_404(school, pk=sch_id)
    yr     = currentacademicyr.objects.get(school_name=sdata)
    year   = academicyr.objects.get(acad_year=yr, school_name=sdata)
    return sdata, year


# ─── Dashboard ────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def transport_dashboard(request):
    sdata, year = _base(request)
    sch_id = request.session.get('sch_id')

    today  = date.today()
    cutoff = today + timedelta(days=30)

    vehicles = Vehicle.objects.filter(sch=sdata)
    drivers  = Driver.objects.filter(sch=sdata)
    routes   = Route.objects.filter(sch=sdata)
    allocated = StudentTransport.objects.filter(sch=sdata, is_active=True).count()

    expiry_alerts = []
    for v in vehicles:
        for alert in v.expiring_soon(30):
            alert['vehicle'] = v
            expiry_alerts.append(alert)

    for d in drivers:
        if d.license_expiring_soon(30):
            expiry_alerts.append({
                'vehicle': None,
                'driver': d,
                'doc': 'Driver License',
                'expiry': d.license_expiry,
                'days_left': (d.license_expiry - today).days,
            })

    expiry_alerts.sort(key=lambda x: x['days_left'])

    context = {
        'skool': sdata, 'year': year,
        'total_vehicles':  vehicles.count(),
        'active_vehicles': vehicles.filter(status='Active').count(),
        'maintenance':     vehicles.filter(status='Maintenance').count(),
        'total_drivers':   drivers.count(),
        'total_routes':    routes.count(),
        'active_routes':   routes.filter(is_active=True).count(),
        'total_stops':     Stop.objects.filter(route__sch=sdata).count(),
        'allocated_students': allocated,
        'expiry_alerts':   expiry_alerts[:10],
    }
    return render(request, 'transport/dashboard.html', context)


# ─── Vehicle Type ─────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def vehicle_type_list(request):
    sdata, year = _base(request)
    data = VehicleType.objects.filter(sch=sdata)
    if request.method == 'POST':
        form = VehicleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle type added.')
            return redirect('vehicle_type_list')
    else:
        form = VehicleTypeForm(initial={'sch': sdata})
    return render(request, 'transport/vehicle_type_list.html', {'data': data, 'form': form, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def vehicle_type_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(VehicleType, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Vehicle type deleted.')
    return redirect('vehicle_type_list')


# ─── Vehicle ──────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def vehicle_list(request):
    sdata, year = _base(request)
    vehicles = Vehicle.objects.filter(sch=sdata).select_related('vehicle_type')
    return render(request, 'transport/vehicle_list.html', {'vehicles': vehicles, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def vehicle_add(request):
    sdata, year = _base(request)
    if request.method == 'POST':
        form = VehicleForm(request.POST, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(initial={'sch': sdata}, sch=sdata)
    return render(request, 'transport/vehicle_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Add Vehicle'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def vehicle_edit(request, pk):
    sdata, year = _base(request)
    vehicle = get_object_or_404(Vehicle, pk=pk, sch=sdata)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle, sch=sdata)
    return render(request, 'transport/vehicle_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Edit Vehicle', 'vehicle': vehicle})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def vehicle_delete(request, pk):
    sdata, _ = _base(request)
    vehicle = get_object_or_404(Vehicle, pk=pk, sch=sdata)
    vehicle.delete()
    messages.success(request, 'Vehicle deleted.')
    return redirect('vehicle_list')


# ─── Driver ───────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def driver_list(request):
    sdata, year = _base(request)
    drivers = Driver.objects.filter(sch=sdata).select_related('assigned_vehicle')
    return render(request, 'transport/driver_list.html', {'drivers': drivers, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def driver_add(request):
    sdata, year = _base(request)
    if request.method == 'POST':
        form = DriverForm(request.POST, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver added successfully.')
            return redirect('driver_list')
    else:
        form = DriverForm(initial={'sch': sdata}, sch=sdata)
    return render(request, 'transport/driver_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Add Driver'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def driver_edit(request, pk):
    sdata, year = _base(request)
    driver = get_object_or_404(Driver, pk=pk, sch=sdata)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated.')
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver, sch=sdata)
    return render(request, 'transport/driver_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Edit Driver', 'driver': driver})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def driver_delete(request, pk):
    sdata, _ = _base(request)
    driver = get_object_or_404(Driver, pk=pk, sch=sdata)
    driver.delete()
    messages.success(request, 'Driver deleted.')
    return redirect('driver_list')


# ─── Route ────────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def route_list(request):
    sdata, year = _base(request)
    routes = Route.objects.filter(sch=sdata).select_related('vehicle', 'driver')
    return render(request, 'transport/route_list.html', {'routes': routes, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def route_add(request):
    sdata, year = _base(request)
    if request.method == 'POST':
        form = RouteForm(request.POST, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route added.')
            return redirect('route_list')
    else:
        form = RouteForm(initial={'sch': sdata}, sch=sdata)
    return render(request, 'transport/route_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Add Route'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def route_edit(request, pk):
    sdata, year = _base(request)
    route = get_object_or_404(Route, pk=pk, sch=sdata)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route updated.')
            return redirect('route_list')
    else:
        form = RouteForm(instance=route, sch=sdata)
    return render(request, 'transport/route_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Edit Route', 'route': route})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def route_delete(request, pk):
    sdata, _ = _base(request)
    route = get_object_or_404(Route, pk=pk, sch=sdata)
    route.delete()
    messages.success(request, 'Route deleted.')
    return redirect('route_list')


# ─── Stops ────────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def stop_list(request, route_pk):
    sdata, year = _base(request)
    route = get_object_or_404(Route, pk=route_pk, sch=sdata)
    stops = route.stops.all()
    return render(request, 'transport/stop_list.html', {'route': route, 'stops': stops, 'skool': sdata, 'year': year})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def stop_add(request, route_pk):
    sdata, year = _base(request)
    route = get_object_or_404(Route, pk=route_pk, sch=sdata)
    if request.method == 'POST':
        form = StopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)
            stop.route = route
            stop.save()
            messages.success(request, 'Stop added.')
            return redirect('stop_list', route_pk=route.pk)
    else:
        next_seq = route.stops.count() + 1
        form = StopForm(initial={'sequence': next_seq})
    return render(request, 'transport/stop_form.html', {'form': form, 'route': route, 'skool': sdata, 'year': year, 'title': 'Add Stop'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def stop_edit(request, pk):
    sdata, year = _base(request)
    stop = get_object_or_404(Stop, pk=pk, route__sch=sdata)
    if request.method == 'POST':
        form = StopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stop updated.')
            return redirect('stop_list', route_pk=stop.route.pk)
    else:
        form = StopForm(instance=stop)
    return render(request, 'transport/stop_form.html', {'form': form, 'route': stop.route, 'skool': sdata, 'year': year, 'title': 'Edit Stop', 'stop': stop})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def stop_delete(request, pk):
    sdata, _ = _base(request)
    stop = get_object_or_404(Stop, pk=pk, route__sch=sdata)
    route_pk = stop.route.pk
    stop.delete()
    messages.success(request, 'Stop deleted.')
    return redirect('stop_list', route_pk=route_pk)


# ─── Student Allocation ───────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def allocation_list(request):
    sdata, year = _base(request)
    allocations = (StudentTransport.objects
                   .filter(sch=sdata)
                   .select_related('student', 'route', 'stop')
                   .order_by('route__route_name', 'stop__sequence'))
    routes = Route.objects.filter(sch=sdata, is_active=True)
    selected_route = request.GET.get('route')
    if selected_route:
        allocations = allocations.filter(route_id=selected_route)
    return render(request, 'transport/allocation_list.html', {
        'allocations': allocations, 'routes': routes,
        'selected_route': selected_route,
        'skool': sdata, 'year': year,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def allocation_add(request):
    sdata, year = _base(request)
    if request.method == 'POST':
        form = StudentTransportForm(request.POST, sch=sdata)
        if form.is_valid():
            alloc = form.save(commit=False)
            # deactivate any existing allocation for this student
            StudentTransport.objects.filter(student=alloc.student, is_active=True).update(is_active=False)
            alloc.save()
            messages.success(request, f'{alloc.student} allocated to {alloc.route}.')
            return redirect('allocation_list')
    else:
        form = StudentTransportForm(initial={'sch': sdata, 'start_date': date.today()}, sch=sdata)
    return render(request, 'transport/allocation_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Allocate Student'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def allocation_edit(request, pk):
    sdata, year = _base(request)
    alloc = get_object_or_404(StudentTransport, pk=pk, sch=sdata)
    if request.method == 'POST':
        form = StudentTransportForm(request.POST, instance=alloc, sch=sdata)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allocation updated.')
            return redirect('allocation_list')
    else:
        form = StudentTransportForm(instance=alloc, sch=sdata)
    return render(request, 'transport/allocation_form.html', {'form': form, 'skool': sdata, 'year': year, 'title': 'Edit Allocation', 'alloc': alloc})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def allocation_delete(request, pk):
    sdata, _ = _base(request)
    alloc = get_object_or_404(StudentTransport, pk=pk, sch=sdata)
    alloc.delete()
    messages.success(request, 'Allocation removed.')
    return redirect('allocation_list')


# ─── AJAX: stops for a route ──────────────────────────────────────────────────

def stops_for_route(request):
    route_id = request.GET.get('route_id')
    stops = Stop.objects.filter(route_id=route_id).order_by('sequence')
    data  = [{'id': s.id, 'name': f"{s.stop_name} — ₹{s.monthly_fee}/mo"} for s in stops]
    return JsonResponse({'stops': data})


# ─── GPS: inbound position push ───────────────────────────────────────────────

@csrf_exempt
def gps_push(request):
    """
    Generic HTTP GPS push endpoint.
    Accepts JSON POST:
      {
        "device_id": "IMEI or GPS device ID stored on Vehicle.gps_device_id",
        "lat": 11.0168,
        "lng": 76.9558,
        "speed": 40.5,
        "heading": 270,
        "timestamp": "2024-06-30T08:32:00Z"   // ISO-8601 UTC
      }
    Compatible with: AIS-140 HTTP forwarders, Flespi webhooks, custom trackers.
    No auth required — callers use the device_id as the shared secret.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    device_id = body.get('device_id') or body.get('imei') or body.get('vehicle_id')
    lat       = body.get('lat') or body.get('latitude')
    lng       = body.get('lng') or body.get('longitude')
    speed     = body.get('speed', 0)
    heading   = body.get('heading', 0)
    ts_raw    = body.get('timestamp') or body.get('ts')

    if not all([device_id, lat, lng]):
        return JsonResponse({'error': 'device_id, lat, lng required'}, status=400)

    vehicle = Vehicle.objects.filter(gps_device_id=device_id).first()
    if not vehicle:
        return JsonResponse({'error': 'Unknown device_id'}, status=404)

    if ts_raw:
        from django.utils.dateparse import parse_datetime
        ts = parse_datetime(str(ts_raw)) or timezone.now()
    else:
        ts = timezone.now()

    VehiclePosition.objects.update_or_create(
        vehicle=vehicle,
        defaults={
            'latitude': lat, 'longitude': lng,
            'speed_kmh': speed, 'heading': heading,
            'timestamp': ts,
        }
    )
    VehiclePositionHistory.objects.create(
        vehicle=vehicle, latitude=lat, longitude=lng,
        speed_kmh=speed, heading=heading, timestamp=ts,
    )
    return JsonResponse({'status': 'ok'})


# ─── GPS: live positions JSON (for map polling) ───────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gps_positions(request):
    """Returns current positions of all school vehicles as JSON for the live map."""
    sdata, _ = _base(request)
    positions = (VehiclePosition.objects
                 .filter(vehicle__sch=sdata)
                 .select_related('vehicle'))
    data = []
    for p in positions:
        data.append({
            'vehicle_id':   p.vehicle.pk,
            'vehicle_name': str(p.vehicle),
            'vehicle_number': p.vehicle.vehicle_number,
            'lat':          float(p.latitude),
            'lng':          float(p.longitude),
            'speed':        float(p.speed_kmh),
            'heading':      p.heading,
            'timestamp':    p.timestamp.isoformat(),
        })
    return JsonResponse({'positions': data})


# ─── GPS: live map view ────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def live_map(request):
    sdata, year = _base(request)
    gps_cfg, _ = GpsSettings.objects.get_or_create(sch=sdata)
    vehicles = Vehicle.objects.filter(sch=sdata, status='Active').prefetch_related('position')
    return render(request, 'transport/live_map.html', {
        'skool': sdata, 'year': year,
        'gps_cfg': gps_cfg,
        'vehicles': vehicles,
    })


# ─── GPS: settings ────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def gps_settings(request):
    sdata, year = _base(request)
    cfg, _ = GpsSettings.objects.get_or_create(sch=sdata)
    if request.method == 'POST':
        cfg.mappls_api_key = request.POST.get('mappls_api_key', '').strip()
        cfg.save()
        messages.success(request, 'GPS settings saved.')
        return redirect('gps_settings')
    vehicles = Vehicle.objects.filter(sch=sdata).order_by('vehicle_name')
    return render(request, 'transport/gps_settings.html', {
        'skool': sdata, 'year': year, 'cfg': cfg, 'vehicles': vehicles,
    })


# ─── Boarding Attendance ──────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def boarding_attendance(request):
    """
    Landing page: filter by route + date + trip, then show the attendance sheet
    or redirect to the mark page.
    """
    sdata, year = _base(request)
    routes = Route.objects.filter(sch=sdata, is_active=True)

    route_id  = request.GET.get('route')
    att_date  = request.GET.get('date', date.today().isoformat())
    trip      = request.GET.get('trip', 'AM')

    records   = None
    route_obj = None
    summary   = {}

    if route_id:
        route_obj = get_object_or_404(Route, pk=route_id, sch=sdata)

        # All active students on this route grouped by stop
        allocations = (StudentTransport.objects
                       .filter(route=route_obj, is_active=True)
                       .select_related('student', 'stop')
                       .order_by('stop__sequence', 'student__first_name'))

        # Existing attendance records for this trip
        existing = {
            a.student_id: a
            for a in BoardingAttendance.objects.filter(
                route=route_obj, date=att_date, trip=trip
            )
        }

        records = []
        for alloc in allocations:
            att = existing.get(alloc.student_id)
            records.append({
                'alloc':   alloc,
                'student': alloc.student,
                'stop':    alloc.stop,
                'status':  att.status if att else None,
                'att_id':  att.pk if att else None,
            })

        boarded = sum(1 for r in records if r['status'] == 'Boarded')
        absent  = sum(1 for r in records if r['status'] == 'Absent')
        missed  = sum(1 for r in records if r['status'] == 'Missed')
        summary = {'total': len(records), 'boarded': boarded,
                   'absent': absent, 'missed': missed,
                   'unmarked': len(records) - boarded - absent - missed}

    return render(request, 'transport/boarding_attendance.html', {
        'skool': sdata, 'year': year,
        'routes': routes, 'route_obj': route_obj,
        'records': records, 'summary': summary,
        'att_date': att_date, 'trip': trip,
        'selected_route': route_id,
        'trip_choices': BoardingAttendance.TRIP_CHOICES,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def boarding_mark(request):
    """Saves attendance for all students in one POST."""
    if request.method != 'POST':
        return redirect('boarding_attendance')

    sdata, _ = _base(request)
    route_id = request.POST.get('route_id')
    att_date = request.POST.get('date')
    trip     = request.POST.get('trip')

    route_obj = get_object_or_404(Route, pk=route_id, sch=sdata)

    allocations = StudentTransport.objects.filter(
        route=route_obj, is_active=True
    ).select_related('student', 'stop')

    for alloc in allocations:
        status = request.POST.get(f'status_{alloc.student_id}')
        if not status:
            continue
        BoardingAttendance.objects.update_or_create(
            student=alloc.student,
            date=att_date,
            trip=trip,
            defaults={
                'sch':       sdata,
                'route':     route_obj,
                'stop':      alloc.stop,
                'status':    status,
                'marked_by': request.user,
            }
        )

    messages.success(request, f'Boarding attendance saved for {att_date} ({trip}).')
    return redirect(
        f"{request.build_absolute_uri('/transport/boarding/')}?route={route_id}&date={att_date}&trip={trip}"
    )


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def boarding_report(request):
    """Monthly/date-range boarding report per route."""
    sdata, year = _base(request)
    routes    = Route.objects.filter(sch=sdata, is_active=True)
    route_id  = request.GET.get('route')
    from_date = request.GET.get('from', date.today().replace(day=1).isoformat())
    to_date   = request.GET.get('to', date.today().isoformat())
    trip      = request.GET.get('trip', '')

    records = None
    route_obj = None

    if route_id:
        route_obj = get_object_or_404(Route, pk=route_id, sch=sdata)
        qs = (BoardingAttendance.objects
              .filter(route=route_obj, date__range=[from_date, to_date])
              .select_related('student', 'stop'))
        if trip:
            qs = qs.filter(trip=trip)

        from itertools import groupby
        qs = list(qs.order_by('date', 'trip', 'stop__sequence', 'student__first_name'))
        grouped = {}
        for k, g in groupby(qs, key=lambda x: (x.date, x.trip)):
            grouped[k] = list(g)
        records = grouped

    return render(request, 'transport/boarding_report.html', {
        'skool': sdata, 'year': year,
        'routes': routes, 'route_obj': route_obj,
        'records': records,
        'from_date': from_date, 'to_date': to_date,
        'trip': trip, 'selected_route': route_id,
        'trip_choices': BoardingAttendance.TRIP_CHOICES,
    })
