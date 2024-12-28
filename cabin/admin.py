from django.contrib import admin
from .models import Rider, Driver, Car, RideRequest, Ride, Payment


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ('rating', 'x', 'y')


class CarAdmin(admin.TabularInline):
    model = Car


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('rating', 'x', 'y', 'active')
    inlines = (CarAdmin,)


@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('rider', 'x', 'y', 'car_type')


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('pickup_time', 'dropoff_time', 'car', 'request',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ride', 'amount', 'status')
