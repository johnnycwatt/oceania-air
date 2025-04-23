from django.db import models
from django.conf import settings
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )  # Nullable for guest bookings

    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)  # Link to Flight
    booking_reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)  #"BKG-XYZ123"
    number_of_passengers = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    is_guest_booking = models.BooleanField(default=False)

    def __str__(self):
        return self.booking_reference
    
class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=50, blank=True)  #Optional
    email_address = models.EmailField(blank=True)  # Optional
    is_primary_passenger = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    