from django.contrib import admin
from .models import (
    Hostel, Block, Floor, Room, Bed, HostelAdmission,
    RoomTransfer, WaitingList, HostelFeeType, HostelFeeInvoice,
    HostelFeeReceipt, HostelAttendance, LeaveApplication, GatePass,
)

admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(HostelAdmission)
admin.site.register(RoomTransfer)
admin.site.register(WaitingList)
admin.site.register(HostelFeeType)
admin.site.register(HostelFeeInvoice)
admin.site.register(HostelFeeReceipt)
admin.site.register(HostelAttendance)
admin.site.register(LeaveApplication)
admin.site.register(GatePass)
