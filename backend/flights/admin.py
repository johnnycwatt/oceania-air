from django.contrib import admin
from .models import Airport, Aircraft, Flight
from django.contrib.admin.widgets import AdminSplitDateTime
from django.db import models

class FlightAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateTimeField: {'widget': AdminSplitDateTime},
    }
    
    fieldsets = (
        (None, {
            'fields': ('flight_number', 'origin', 'destination', 'aircraft', 'capacity', 'seats_available', 'price', 'status'),
        }),
        ('Flight Times', {
            'fields': ('departure_time', 'arrival_time'),
            'description': 'Enter times in UTC using the format: YYYY-MM-DD HH:MM:SS (24-hour time, e.g., 2023-10-25 14:30:00).',
        }),
    )
    
    # Display key fields in the list view
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'status')
    
    # Add filters for quick sorting
    list_filter = ('status', 'origin', 'destination')
    
    # Enable search by flight number and airport codes
    search_fields = ('flight_number', 'origin__icao_code', 'destination__icao_code')
    
    # Sort flights by departure time by default
    ordering = ('departure_time',)
    

admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(Flight, FlightAdmin)