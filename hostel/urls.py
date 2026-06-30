from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Dashboard
    path('', login_required(views.hostel_dashboard), name='hostel_dashboard'),

    # Hostel Master
    path('hostels/',                       login_required(views.hostel_list),    name='hostel_list'),
    path('hostels/add/',                   login_required(views.hostel_add),     name='hostel_add'),
    path('hostels/<int:pk>/edit/',         login_required(views.hostel_edit),    name='hostel_edit'),
    path('hostels/<int:pk>/delete/',       login_required(views.hostel_delete),  name='hostel_delete'),

    # Blocks
    path('hostels/<int:hostel_pk>/blocks/',       login_required(views.block_list), name='block_list'),
    path('hostels/<int:hostel_pk>/blocks/add/',   login_required(views.block_add),  name='block_add'),
    path('blocks/<int:pk>/edit/',                 login_required(views.block_edit), name='block_edit'),
    path('blocks/<int:pk>/delete/',               login_required(views.block_delete), name='block_delete'),

    # Floors
    path('blocks/<int:block_pk>/floors/',         login_required(views.floor_list), name='floor_list'),
    path('blocks/<int:block_pk>/floors/add/',     login_required(views.floor_add),  name='floor_add'),
    path('floors/<int:pk>/edit/',                 login_required(views.floor_edit), name='floor_edit'),
    path('floors/<int:pk>/delete/',               login_required(views.floor_delete), name='floor_delete'),

    # Rooms
    path('blocks/<int:block_pk>/rooms/',          login_required(views.room_list), name='room_list'),
    path('blocks/<int:block_pk>/rooms/add/',      login_required(views.room_add),  name='room_add'),
    path('rooms/<int:pk>/edit/',                  login_required(views.room_edit), name='room_edit'),
    path('rooms/<int:pk>/delete/',                login_required(views.room_delete), name='room_delete'),

    # Beds
    path('rooms/<int:room_pk>/beds/',             login_required(views.bed_list), name='bed_list'),
    path('rooms/<int:room_pk>/beds/add/',         login_required(views.bed_add),  name='bed_add'),
    path('beds/<int:pk>/edit/',                   login_required(views.bed_edit), name='bed_edit'),
    path('beds/<int:pk>/delete/',                 login_required(views.bed_delete), name='bed_delete'),

    # Admissions
    path('admissions/',                    login_required(views.admission_list),   name='hostel_admission_list'),
    path('admissions/add/',                login_required(views.admission_add),    name='hostel_admission_add'),
    path('admissions/<int:pk>/edit/',      login_required(views.admission_edit),   name='hostel_admission_edit'),
    path('admissions/<int:pk>/vacate/',    login_required(views.admission_delete), name='hostel_admission_delete'),

    # Transfers
    path('transfers/',                     login_required(views.transfer_list), name='hostel_transfer_list'),
    path('transfers/add/',                 login_required(views.transfer_add),  name='hostel_transfer_add'),

    # Waiting List
    path('waiting/',                       login_required(views.waiting_list),   name='hostel_waiting_list'),
    path('waiting/add/',                   login_required(views.waiting_add),    name='hostel_waiting_add'),
    path('waiting/<int:pk>/edit/',         login_required(views.waiting_edit),   name='hostel_waiting_edit'),
    path('waiting/<int:pk>/delete/',       login_required(views.waiting_delete), name='hostel_waiting_delete'),

    # Fee Types
    path('fee-types/',                     login_required(views.fee_type_list),   name='hostel_fee_type_list'),
    path('fee-types/add/',                 login_required(views.fee_type_add),    name='hostel_fee_type_add'),
    path('fee-types/<int:pk>/edit/',       login_required(views.fee_type_edit),   name='hostel_fee_type_edit'),
    path('fee-types/<int:pk>/delete/',     login_required(views.fee_type_delete), name='hostel_fee_type_delete'),

    # Fee Invoices
    path('fees/',                          login_required(views.fee_invoice_list),   name='hostel_fee_invoice_list'),
    path('fees/add/',                      login_required(views.fee_invoice_add),    name='hostel_fee_invoice_add'),
    path('fees/<int:pk>/delete/',          login_required(views.fee_invoice_delete), name='hostel_fee_invoice_delete'),

    # Receipts
    path('fees/<int:invoice_pk>/pay/',     login_required(views.fee_receipt_add), name='hostel_fee_receipt_add'),

    # Attendance
    path('attendance/',                    login_required(views.hostel_attendance),        name='hostel_attendance'),
    path('attendance/mark/',               login_required(views.hostel_attendance_mark),   name='hostel_attendance_mark'),
    path('attendance/report/',             login_required(views.hostel_attendance_report), name='hostel_attendance_report'),

    # Leave
    path('leave/',                         login_required(views.leave_list),    name='hostel_leave_list'),
    path('leave/add/',                     login_required(views.leave_add),     name='hostel_leave_add'),
    path('leave/<int:pk>/approve/',        login_required(views.leave_approve), name='hostel_leave_approve'),
    path('leave/<int:pk>/reject/',         login_required(views.leave_reject),  name='hostel_leave_reject'),
    path('leave/<int:pk>/return/',         login_required(views.leave_return),  name='hostel_leave_return'),

    # Gate Pass
    path('gatepass/',                      login_required(views.gatepass_list),   name='hostel_gatepass_list'),
    path('gatepass/add/',                  login_required(views.gatepass_add),    name='hostel_gatepass_add'),
    path('gatepass/<int:pk>/return/',      login_required(views.gatepass_return), name='hostel_gatepass_return'),
    path('gatepass/<int:pk>/delete/',      login_required(views.gatepass_delete), name='hostel_gatepass_delete'),

    # AJAX
    path('ajax/blocks/',                   views.ajax_blocks_for_hostel, name='ajax_blocks_for_hostel'),
    path('ajax/rooms/',                    views.ajax_rooms_for_block,   name='ajax_rooms_for_block'),
    path('ajax/beds/',                     views.ajax_beds_for_room,     name='ajax_beds_for_room'),
]
