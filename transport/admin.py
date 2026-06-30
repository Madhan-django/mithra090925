from django.contrib import admin
from .models import VehicleType, Vehicle, Driver, Route, Stop, StudentTransport

admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(StudentTransport)
