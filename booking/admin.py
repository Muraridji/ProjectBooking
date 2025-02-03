from django.contrib import admin
from booking.models import Place, Booking

# Register your models here.
@admin.register(Place)
class AdminPlace(admin.ModelAdmin):
    list_display = ('title', 'price', 'capacity', 'is_available')

@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    pass