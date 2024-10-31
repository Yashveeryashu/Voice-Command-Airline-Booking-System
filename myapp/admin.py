# admin.py
from django.contrib import admin
from .models import FlightBooking

class FlightBookingAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('trip_type', 'from_location', 'to_location', 'departure_date', 'return_date', 'passengers', 'travel_class')
    
    # Add search functionality for specific fields
    search_fields = ('from_location', 'to_location')
    
    # Filter options to quickly view by fields
    list_filter = ('trip_type', 'travel_class', 'departure_date')

# Register the model and the custom admin interface
admin.site.register(FlightBooking, FlightBookingAdmin)
