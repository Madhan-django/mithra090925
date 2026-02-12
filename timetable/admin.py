# admin.py
from django.contrib import admin
from .models import TimeSlot, Timetable,TeachingAllocation,ReservedSlot

admin.site.register([TimeSlot, Timetable,TeachingAllocation,ReservedSlot])
