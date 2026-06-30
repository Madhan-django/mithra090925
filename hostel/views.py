from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date

from institutions.models import school
from setup.models import currentacademicyr, academicyr
from authenticate.decorators import allowed_users

from .models import (
    Hostel, Block, Floor, Room, Bed, HostelAdmission,
    RoomTransfer, WaitingList, HostelFeeType, HostelFeeInvoice,
    HostelFeeReceipt, HostelAttendance, LeaveApplication, GatePass,
)
from .forms import (
    HostelForm, BlockForm, FloorForm, RoomForm, BedForm,
    HostelAdmissionForm, RoomTransferForm, WaitingListForm,
    HostelFeeTypeForm, HostelFeeInvoiceForm, HostelFeeReceiptForm,
    LeaveApplicationForm, GatePassForm,
)


def _base(request):
    sch_id = request.session.get('sch_id')
    sdata  = get_object_or_404(school, pk=sch_id)
    yr     = currentacademicyr.objects.get(school_name=sdata)
    year   = academicyr.objects.get(acad_year=yr, school_name=sdata)
    return sdata, year


# ─── Dashboard ────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def hostel_dashboard(request):
    sdata, year = _base(request)

    hostels   = Hostel.objects.filter(sch=sdata)
    total_beds = Bed.objects.filter(room__block__hostel__sch=sdata).count()
    occupied   = Bed.objects.filter(room__block__hostel__sch=sdata, status='Occupied').count()
    available  = total_beds - occupied
    admissions = HostelAdmission.objects.filter(sch=sdata, status='Active').count()

    pending_leaves   = LeaveApplication.objects.filter(sch=sdata, status='Pending').count()
    open_gatepasses  = GatePass.objects.filter(sch=sdata, status='Open').count()
    waiting          = WaitingList.objects.filter(sch=sdata, status='Waiting').count()
    pending_invoices = HostelFeeInvoice.objects.filter(sch=sdata, status='Pending').count()

    recent_admissions = HostelAdmission.objects.filter(sch=sdata, status='Active').select_related(
        'student', 'hostel', 'room', 'bed'
    )[:8]

    context = {
        'skool': sdata, 'year': year,
        'total_hostels':    hostels.count(),
        'active_hostels':   hostels.filter(status='Active').count(),
        'total_beds':       total_beds,
        'occupied_beds':    occupied,
        'available_beds':   available,
        'total_admissions': admissions,
        'pending_leaves':   pending_leaves,
        'open_gatepasses':  open_gatepasses,
        'waiting_count':    waiting,
        'pending_invoices': pending_invoices,
        'hostels':          hostels,
        'recent_admissions': recent_admissions,
        'occupancy_pct': round((occupied / total_beds * 100) if total_beds else 0),
    }
    return render(request, 'hostel/dashboard.html', context)


# ─── Hostel CRUD ──────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def hostel_list(request):
    sdata, year = _base(request)
    hostels = Hostel.objects.filter(sch=sdata)
    return render(request, 'hostel/hostel_list.html', {'skool': sdata, 'year': year, 'hostels': hostels})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def hostel_add(request):
    sdata, year = _base(request)
    form = HostelForm(request.POST or None, initial={'sch': sdata})
    if form.is_valid():
        form.save()
        messages.success(request, 'Hostel added successfully.')
        return redirect('hostel_list')
    return render(request, 'hostel/hostel_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Add Hostel'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def hostel_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(Hostel, pk=pk, sch=sdata)
    form = HostelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Hostel updated.')
        return redirect('hostel_list')
    return render(request, 'hostel/hostel_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Edit Hostel'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def hostel_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(Hostel, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Hostel deleted.')
    return redirect('hostel_list')


# ─── Block CRUD ───────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def block_list(request, hostel_pk):
    sdata, year = _base(request)
    hostel = get_object_or_404(Hostel, pk=hostel_pk, sch=sdata)
    blocks = Block.objects.filter(hostel=hostel)
    return render(request, 'hostel/block_list.html', {'skool': sdata, 'year': year, 'hostel': hostel, 'blocks': blocks})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def block_add(request, hostel_pk):
    sdata, year = _base(request)
    hostel = get_object_or_404(Hostel, pk=hostel_pk, sch=sdata)
    form = BlockForm(request.POST or None, initial={'hostel': hostel}, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Block added.')
        return redirect('block_list', hostel_pk=hostel_pk)
    return render(request, 'hostel/block_form.html', {'skool': sdata, 'year': year, 'form': form, 'hostel': hostel, 'title': 'Add Block'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def block_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(Block, pk=pk, hostel__sch=sdata)
    form = BlockForm(request.POST or None, instance=obj, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Block updated.')
        return redirect('block_list', hostel_pk=obj.hostel_id)
    return render(request, 'hostel/block_form.html', {'skool': sdata, 'year': year, 'form': form, 'hostel': obj.hostel, 'title': 'Edit Block'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def block_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(Block, pk=pk, hostel__sch=sdata)
    hostel_pk = obj.hostel_id
    obj.delete()
    messages.success(request, 'Block deleted.')
    return redirect('block_list', hostel_pk=hostel_pk)


# ─── Floor CRUD ───────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def floor_list(request, block_pk):
    sdata, year = _base(request)
    block  = get_object_or_404(Block, pk=block_pk, hostel__sch=sdata)
    floors = Floor.objects.filter(block=block)
    return render(request, 'hostel/floor_list.html', {'skool': sdata, 'year': year, 'block': block, 'floors': floors})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def floor_add(request, block_pk):
    sdata, year = _base(request)
    block = get_object_or_404(Block, pk=block_pk, hostel__sch=sdata)
    form  = FloorForm(request.POST or None, initial={'block': block})
    if form.is_valid():
        form.save()
        messages.success(request, 'Floor added.')
        return redirect('floor_list', block_pk=block_pk)
    return render(request, 'hostel/floor_form.html', {'skool': sdata, 'year': year, 'form': form, 'block': block, 'title': 'Add Floor'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def floor_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(Floor, pk=pk, block__hostel__sch=sdata)
    form = FloorForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Floor updated.')
        return redirect('floor_list', block_pk=obj.block_id)
    return render(request, 'hostel/floor_form.html', {'skool': sdata, 'year': year, 'form': form, 'block': obj.block, 'title': 'Edit Floor'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def floor_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(Floor, pk=pk, block__hostel__sch=sdata)
    block_pk = obj.block_id
    obj.delete()
    messages.success(request, 'Floor deleted.')
    return redirect('floor_list', block_pk=block_pk)


# ─── Room CRUD ────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def room_list(request, block_pk):
    sdata, year = _base(request)
    block = get_object_or_404(Block, pk=block_pk, hostel__sch=sdata)
    rooms = Room.objects.filter(block=block).prefetch_related('beds')
    return render(request, 'hostel/room_list.html', {'skool': sdata, 'year': year, 'block': block, 'rooms': rooms})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def room_add(request, block_pk):
    sdata, year = _base(request)
    block = get_object_or_404(Block, pk=block_pk, hostel__sch=sdata)
    form  = RoomForm(request.POST or None, initial={'block': block}, block=block)
    if form.is_valid():
        form.save()
        messages.success(request, 'Room added.')
        return redirect('room_list', block_pk=block_pk)
    return render(request, 'hostel/room_form.html', {'skool': sdata, 'year': year, 'form': form, 'block': block, 'title': 'Add Room'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def room_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(Room, pk=pk, block__hostel__sch=sdata)
    form = RoomForm(request.POST or None, instance=obj, block=obj.block)
    if form.is_valid():
        form.save()
        messages.success(request, 'Room updated.')
        return redirect('room_list', block_pk=obj.block_id)
    return render(request, 'hostel/room_form.html', {'skool': sdata, 'year': year, 'form': form, 'block': obj.block, 'title': 'Edit Room'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def room_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(Room, pk=pk, block__hostel__sch=sdata)
    block_pk = obj.block_id
    obj.delete()
    messages.success(request, 'Room deleted.')
    return redirect('room_list', block_pk=block_pk)


# ─── Bed CRUD ─────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def bed_list(request, room_pk):
    sdata, year = _base(request)
    room = get_object_or_404(Room, pk=room_pk, block__hostel__sch=sdata)
    beds = Bed.objects.filter(room=room)
    return render(request, 'hostel/bed_list.html', {'skool': sdata, 'year': year, 'room': room, 'beds': beds})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def bed_add(request, room_pk):
    sdata, year = _base(request)
    room = get_object_or_404(Room, pk=room_pk, block__hostel__sch=sdata)
    form = BedForm(request.POST or None, initial={'room': room})
    if form.is_valid():
        form.save()
        messages.success(request, 'Bed added.')
        return redirect('bed_list', room_pk=room_pk)
    return render(request, 'hostel/bed_form.html', {'skool': sdata, 'year': year, 'form': form, 'room': room, 'title': 'Add Bed'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def bed_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(Bed, pk=pk, room__block__hostel__sch=sdata)
    form = BedForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bed updated.')
        return redirect('bed_list', room_pk=obj.room_id)
    return render(request, 'hostel/bed_form.html', {'skool': sdata, 'year': year, 'form': form, 'room': obj.room, 'title': 'Edit Bed'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def bed_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(Bed, pk=pk, room__block__hostel__sch=sdata)
    room_pk = obj.room_id
    obj.delete()
    messages.success(request, 'Bed deleted.')
    return redirect('bed_list', room_pk=room_pk)


# ─── Admission CRUD ───────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def admission_list(request):
    sdata, year = _base(request)
    admissions = HostelAdmission.objects.filter(sch=sdata).select_related('student', 'hostel', 'room', 'bed')
    hostel_filter = request.GET.get('hostel')
    status_filter = request.GET.get('status', 'Active')
    if hostel_filter:
        admissions = admissions.filter(hostel_id=hostel_filter)
    if status_filter:
        admissions = admissions.filter(status=status_filter)
    hostels = Hostel.objects.filter(sch=sdata)
    return render(request, 'hostel/admission_list.html', {
        'skool': sdata, 'year': year,
        'admissions': admissions, 'hostels': hostels,
        'hostel_filter': hostel_filter, 'status_filter': status_filter,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def admission_add(request):
    sdata, year = _base(request)
    form = HostelAdmissionForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student admitted to hostel.')
        return redirect('hostel_admission_list')
    return render(request, 'hostel/admission_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'New Admission'})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def admission_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(HostelAdmission, pk=pk, sch=sdata)
    form = HostelAdmissionForm(request.POST or None, instance=obj, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Admission updated.')
        return redirect('hostel_admission_list')
    return render(request, 'hostel/admission_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Edit Admission'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def admission_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(HostelAdmission, pk=pk, sch=sdata)
    obj.status = 'Vacated'
    obj.save()
    messages.success(request, 'Admission vacated.')
    return redirect('hostel_admission_list')


# ─── Room Transfer ────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def transfer_list(request):
    sdata, year = _base(request)
    transfers = RoomTransfer.objects.filter(sch=sdata).select_related('student', 'from_bed', 'to_bed')
    return render(request, 'hostel/transfer_list.html', {'skool': sdata, 'year': year, 'transfers': transfers})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def transfer_add(request):
    sdata, year = _base(request)
    form = RoomTransferForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        transfer = form.save(commit=False)
        transfer.approved_by = request.user
        transfer.save()
        # Update admission record
        admission = HostelAdmission.objects.filter(
            sch=sdata, student=transfer.student, bed=transfer.from_bed, status='Active'
        ).first()
        if admission:
            admission.bed   = transfer.to_bed
            admission.room  = transfer.to_bed.room
            admission.block = transfer.to_bed.room.block
            admission.floor = transfer.to_bed.room.floor
            admission.status = 'Transferred'
            admission.save()
            new_admission = HostelAdmission(
                sch=sdata, student=transfer.student,
                hostel=transfer.to_bed.room.block.hostel,
                block=transfer.to_bed.room.block,
                floor=transfer.to_bed.room.floor,
                room=transfer.to_bed.room, bed=transfer.to_bed,
                admission_date=transfer.transfer_date,
                ac_year=admission.ac_year,
                emergency_contact=admission.emergency_contact,
                parent_contact=admission.parent_contact,
                status='Active',
            )
            new_admission.save()
        messages.success(request, 'Room transfer recorded.')
        return redirect('hostel_transfer_list')
    return render(request, 'hostel/transfer_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'New Transfer'})


# ─── Waiting List ─────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin'])
def waiting_list(request):
    sdata, year = _base(request)
    entries = WaitingList.objects.filter(sch=sdata).select_related('student', 'hostel')
    return render(request, 'hostel/waiting_list.html', {'skool': sdata, 'year': year, 'entries': entries})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def waiting_add(request):
    sdata, year = _base(request)
    form = WaitingListForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Added to waiting list.')
        return redirect('hostel_waiting_list')
    return render(request, 'hostel/waiting_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Add to Waiting List'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def waiting_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(WaitingList, pk=pk, sch=sdata)
    form = WaitingListForm(request.POST or None, instance=obj, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Waiting list entry updated.')
        return redirect('hostel_waiting_list')
    return render(request, 'hostel/waiting_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Edit Waiting Entry'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def waiting_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(WaitingList, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Entry removed from waiting list.')
    return redirect('hostel_waiting_list')


# ─── Fee Types ────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_type_list(request):
    sdata, year = _base(request)
    fee_types = HostelFeeType.objects.filter(sch=sdata).select_related('hostel')
    return render(request, 'hostel/fee_type_list.html', {'skool': sdata, 'year': year, 'fee_types': fee_types})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def fee_type_add(request):
    sdata, year = _base(request)
    form = HostelFeeTypeForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fee type added.')
        return redirect('hostel_fee_type_list')
    return render(request, 'hostel/fee_type_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Add Fee Type'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def fee_type_edit(request, pk):
    sdata, year = _base(request)
    obj  = get_object_or_404(HostelFeeType, pk=pk, sch=sdata)
    form = HostelFeeTypeForm(request.POST or None, instance=obj, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Fee type updated.')
        return redirect('hostel_fee_type_list')
    return render(request, 'hostel/fee_type_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Edit Fee Type'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def fee_type_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(HostelFeeType, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Fee type deleted.')
    return redirect('hostel_fee_type_list')


# ─── Fee Invoices ─────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_invoice_list(request):
    sdata, year = _base(request)
    invoices = HostelFeeInvoice.objects.filter(sch=sdata).select_related('student', 'fee_type')
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    return render(request, 'hostel/fee_invoice_list.html', {
        'skool': sdata, 'year': year, 'invoices': invoices, 'status_filter': status_filter,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_invoice_add(request):
    sdata, year = _base(request)
    form = HostelFeeInvoiceForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        invoice = form.save(commit=False)
        last = HostelFeeInvoice.objects.filter(sch=sdata).order_by('-id').first()
        invoice.invoice_no = f"HF{(last.id + 1 if last else 1):04d}"
        invoice.save()
        messages.success(request, 'Invoice created.')
        return redirect('hostel_fee_invoice_list')
    return render(request, 'hostel/fee_invoice_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Create Invoice'})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_invoice_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(HostelFeeInvoice, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Invoice deleted.')
    return redirect('hostel_fee_invoice_list')


# ─── Fee Receipt ──────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def fee_receipt_add(request, invoice_pk):
    sdata, year = _base(request)
    invoice = get_object_or_404(HostelFeeInvoice, pk=invoice_pk, sch=sdata)
    form = HostelFeeReceiptForm(request.POST or None, initial={'invoice': invoice})
    if form.is_valid():
        receipt = form.save(commit=False)
        receipt.received_by = request.user
        receipt.save()
        paid = invoice.amount_paid()
        if paid >= invoice.net_amount():
            invoice.status = 'Paid'
        elif paid > 0:
            invoice.status = 'Partial'
        invoice.save(update_fields=['status'])
        messages.success(request, 'Receipt recorded.')
        return redirect('hostel_fee_invoice_list')
    return render(request, 'hostel/fee_receipt_form.html', {'skool': sdata, 'year': year, 'form': form, 'invoice': invoice, 'title': 'Record Payment'})


# ─── Attendance ───────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def hostel_attendance(request):
    sdata, year = _base(request)
    hostels = Hostel.objects.filter(sch=sdata, status='Active')
    hostel_id = request.GET.get('hostel')
    att_date  = request.GET.get('date', str(date.today()))
    session   = request.GET.get('session', 'Night')

    admissions = []
    attendance_map = {}
    selected_hostel = None

    if hostel_id:
        selected_hostel = get_object_or_404(Hostel, pk=hostel_id, sch=sdata)
        admissions = HostelAdmission.objects.filter(
            hostel=selected_hostel, status='Active'
        ).select_related('student')
        records = HostelAttendance.objects.filter(
            hostel=selected_hostel, date=att_date, session=session
        )
        attendance_map = {r.student_id: r.status for r in records}

    return render(request, 'hostel/attendance.html', {
        'skool': sdata, 'year': year,
        'hostels': hostels, 'selected_hostel': selected_hostel,
        'admissions': admissions, 'attendance_map': attendance_map,
        'att_date': att_date, 'session': session,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def hostel_attendance_mark(request):
    if request.method != 'POST':
        return redirect('hostel_attendance')
    sdata, _ = _base(request)
    hostel_id = request.POST.get('hostel')
    att_date  = request.POST.get('date')
    session   = request.POST.get('session')
    hostel    = get_object_or_404(Hostel, pk=hostel_id, sch=sdata)

    admissions = HostelAdmission.objects.filter(hostel=hostel, status='Active')
    for adm in admissions:
        status = request.POST.get(f'status_{adm.student_id}', 'Absent')
        HostelAttendance.objects.update_or_create(
            sch=sdata, hostel=hostel, student=adm.student,
            date=att_date, session=session,
            defaults={'status': status, 'marked_by': request.user},
        )
    messages.success(request, f'Attendance saved for {att_date} — {session}.')
    return redirect(f'/hostel/attendance/?hostel={hostel_id}&date={att_date}&session={session}')


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def hostel_attendance_report(request):
    sdata, year = _base(request)
    hostels = Hostel.objects.filter(sch=sdata, status='Active')
    records = []
    hostel_id  = request.GET.get('hostel')
    from_date  = request.GET.get('from_date', str(date.today()))
    to_date    = request.GET.get('to_date',   str(date.today()))
    session    = request.GET.get('session', '')
    selected_hostel = None

    if hostel_id:
        selected_hostel = get_object_or_404(Hostel, pk=hostel_id, sch=sdata)
        qs = HostelAttendance.objects.filter(
            hostel=selected_hostel, date__range=[from_date, to_date]
        ).select_related('student')
        if session:
            qs = qs.filter(session=session)
        records = qs

    return render(request, 'hostel/attendance_report.html', {
        'skool': sdata, 'year': year,
        'hostels': hostels, 'selected_hostel': selected_hostel,
        'records': records, 'from_date': from_date, 'to_date': to_date, 'session': session,
    })


# ─── Leave Applications ───────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def leave_list(request):
    sdata, year = _base(request)
    leaves = LeaveApplication.objects.filter(sch=sdata).select_related('student', 'hostel')
    status_filter = request.GET.get('status', 'Pending')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    return render(request, 'hostel/leave_list.html', {
        'skool': sdata, 'year': year, 'leaves': leaves, 'status_filter': status_filter,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def leave_add(request):
    sdata, year = _base(request)
    form = LeaveApplicationForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        form.save()
        messages.success(request, 'Leave application submitted.')
        return redirect('hostel_leave_list')
    return render(request, 'hostel/leave_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'New Leave Application'})


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def leave_approve(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(LeaveApplication, pk=pk, sch=sdata)
    obj.status      = 'Approved'
    obj.approved_by = request.user
    obj.save(update_fields=['status', 'approved_by'])
    messages.success(request, 'Leave approved.')
    return redirect('hostel_leave_list')


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def leave_reject(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(LeaveApplication, pk=pk, sch=sdata)
    obj.status           = 'Rejected'
    obj.approved_by      = request.user
    obj.rejection_reason = request.POST.get('reason', '')
    obj.save(update_fields=['status', 'approved_by', 'rejection_reason'])
    messages.success(request, 'Leave rejected.')
    return redirect('hostel_leave_list')


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def leave_return(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(LeaveApplication, pk=pk, sch=sdata)
    obj.status        = 'Returned'
    obj.actual_return = date.today()
    obj.save(update_fields=['status', 'actual_return'])
    messages.success(request, 'Student marked as returned.')
    return redirect('hostel_leave_list')


# ─── Gate Pass ────────────────────────────────────────────────────────────────

@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gatepass_list(request):
    sdata, year = _base(request)
    passes = GatePass.objects.filter(sch=sdata).select_related('student', 'hostel')
    status_filter = request.GET.get('status', '')
    if status_filter:
        passes = passes.filter(status=status_filter)
    return render(request, 'hostel/gatepass_list.html', {
        'skool': sdata, 'year': year, 'passes': passes, 'status_filter': status_filter,
    })


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gatepass_add(request):
    sdata, year = _base(request)
    form = GatePassForm(request.POST or None, initial={'sch': sdata}, sch=sdata)
    if form.is_valid():
        gp = form.save(commit=False)
        gp.approved_by = request.user
        last = GatePass.objects.filter(sch=sdata).order_by('-id').first()
        gp.pass_number = f"GP{(last.id + 1 if last else 1):04d}"
        gp.save()
        messages.success(request, f'Gate pass {gp.pass_number} issued.')
        return redirect('hostel_gatepass_list')
    return render(request, 'hostel/gatepass_form.html', {'skool': sdata, 'year': year, 'form': form, 'title': 'Issue Gate Pass'})


@allowed_users(allowed_roles=['superadmin', 'Admin', 'Accounts'])
def gatepass_return(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(GatePass, pk=pk, sch=sdata)
    obj.actual_return = timezone.now()
    obj.status        = 'Returned'
    obj.save(update_fields=['actual_return', 'status'])
    messages.success(request, f'Gate pass {obj.pass_number} closed — student returned.')
    return redirect('hostel_gatepass_list')


@allowed_users(allowed_roles=['superadmin', 'Admin'])
def gatepass_delete(request, pk):
    sdata, _ = _base(request)
    obj = get_object_or_404(GatePass, pk=pk, sch=sdata)
    obj.delete()
    messages.success(request, 'Gate pass deleted.')
    return redirect('hostel_gatepass_list')


# ─── AJAX ─────────────────────────────────────────────────────────────────────

def ajax_blocks_for_hostel(request):
    hostel_id = request.GET.get('hostel_id')
    blocks = Block.objects.filter(hostel_id=hostel_id, status='Active').values('id', 'name')
    return JsonResponse({'blocks': list(blocks)})


def ajax_rooms_for_block(request):
    block_id = request.GET.get('block_id')
    rooms = Room.objects.filter(block_id=block_id).exclude(status='Maintenance').values('id', 'room_number', 'room_type', 'status')
    return JsonResponse({'rooms': list(rooms)})


def ajax_beds_for_room(request):
    room_id = request.GET.get('room_id')
    beds = Bed.objects.filter(room_id=room_id, status='Available').values('id', 'bed_number')
    return JsonResponse({'beds': list(beds)})
