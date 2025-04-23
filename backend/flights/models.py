from django.db import models

class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    ]
    
    model = models.CharField(max_length=100)  # "SyberJet SJ30i"
    capacity = models.IntegerField()  # 6
    registration_number = models.CharField(max_length=20, unique=True)  #"ZK-OCE"
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
    
    flight_number = models.CharField(max_length=10, unique=True)  #"OA123"
    origin = models.CharField(max_length=100)  #"Dairy Flat (NZNE)"
    destination = models.CharField(max_length=100)  #"Melbourne (YMML)"
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE) #Link to Aircraft
    capacity = models.IntegerField()  #Inherited from aircraft
    seats_available = models.IntegerField()  #Tracks available seats
    price = models.DecimalField(max_digits=10, decimal_places=2)  #250.00
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return self.flight_number