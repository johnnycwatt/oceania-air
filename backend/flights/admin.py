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


admin.site.register(Airport)
admin.site.register(Aircraft)
admin.site.register(Flight, FlightAdmin)