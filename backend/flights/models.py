from django.db import models

# New Airport model
class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)  # e.g., "NZNE"
    name = models.CharField(max_length=100)  # e.g., "Dairy Flat"
    timezone = models.CharField(max_length=10)  # e.g., "GMT+12"

    def __str__(self):
        return f"{self.icao_code} - {self.name}"

class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    ]
    
    model = models.CharField(max_length=100)  # "SyberJet SJ30i"
    capacity = models.IntegerField()  # 6
    registration_number = models.CharField(max_length=20, unique=True)  # "ZK-OCE"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.registration_number

class Flight(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('boarding', 'Boarding'),
        ('departed', 'Departed'),
        ('cancelled', 'Cancelled'),
    ]
    
    flight_number = models.CharField(max_length=10, unique=True)  # "OA123"
    # Replace CharFields with ForeignKeys to Airport
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)  # Link to Aircraft
    capacity = models.IntegerField()  # Inherit from aircraft
    seats_available = models.IntegerField()  # Tracks available seats
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 250.00
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return self.flight_number