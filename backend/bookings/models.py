from django.db import models
import uuid


class Passenger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=50, blank=True)  # Optional
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    passengers = models.ManyToManyField(Passenger, through='BookingPassenger')

    def __str__(self):
        return self.booking_reference

    @property
    def number_of_passengers(self):
        return self.passengers.count()


class BookingPassenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    is_primary_passenger = models.BooleanField(default=False)

    class Meta:
        unique_together = ('booking', 'passenger')  # Prevent duplicate associations

    def __str__(self):
        return f"{self.passenger} in {self.booking}"