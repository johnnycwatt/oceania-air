from rest_framework.test import APITestCase
from rest_framework import status
from bookings.models import Booking, Passenger
from flights.models import Flight, Aircraft, Airport
from core.models import User
from django.utils import timezone

class BookingTests(APITestCase):
    def setUp(self):
        # Create test airports
        self.airport1 = Airport.objects.create(
            icao_code="TEST1", name="Test Airport 1", timezone="GMT+0"
        )
        self.airport2 = Airport.objects.create(
            icao_code="TEST2", name="Test Airport 2", timezone="GMT+0"
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass",
            date_of_birth="1990-01-01",
            phone_number="1234567890"
        )
        
        # Create test aircraft
        self.aircraft = Aircraft.objects.create(
            model="Test Aircraft",
            capacity=5,
            registration_number="ZK-TEST",
            status="active"
        )
        
        # Create test flight using airport instances
        self.flight = Flight.objects.create(
            flight_number="TEST101",
            origin=self.airport1,
            destination=self.airport2,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
            capacity=5,
            seats_available=5,
            price=150.00,
            status="scheduled"
        )
        
        # Create test booking
        self.booking = Booking.objects.create(
            user=self.user,
            flight=self.flight,
            booking_reference="BKG-TEST123",
            number_of_passengers=1,
            total_price=150.00,
            status="confirmed",
            contact_email="test@example.com",
            contact_phone="1234567890",
            is_guest_booking=False
        )
        
        # Create test passenger
        self.passenger = Passenger.objects.create(
            booking=self.booking,
            first_name="Test",
            last_name="Passenger",
            date_of_birth="1990-01-01",
            passport_number="TP123456",
            email_address="test@example.com",
            is_primary_passenger=True
        )

    def test_get_bookings(self):
        response = self.client.get('/api/bookings/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['booking_reference'], "BKG-TEST123")

    def test_create_booking(self):
        flight = Flight.objects.first()
        data = {
            "flight": flight.id,
            "user": None,
            "booking_reference": "BKG-NEW456",
            "number_of_passengers": 2,
            "total_price": 300.00,
            "status": "confirmed",
            "contact_email": "guest@example.com",
            "contact_phone": "0987654321",
            "is_guest_booking": True,
            "passengers": [
                {
                    "first_name": "Guest",
                    "last_name": "One",
                    "date_of_birth": "1980-01-01",
                    "passport_number": "GO123456",
                    "email_address": "guest1@example.com",
                    "is_primary_passenger": True
                },
                {
                    "first_name": "Guest",
                    "last_name": "Two",
                    "date_of_birth": "1982-02-02",
                    "passport_number": "GT789012",
                    "email_address": "guest2@example.com",
                    "is_primary_passenger": False
                }
            ]
        }
        response = self.client.post('/api/bookings/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Passenger.objects.count(), 3)  # 1 from setUp + 2 new

    def test_update_booking(self):
        booking = Booking.objects.first()
        data = {"status": "cancelled"}
        response = self.client.patch(f'/api/bookings/bookings/{booking.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")

    def test_delete_booking(self):
        booking = Booking.objects.first()
        response = self.client.delete(f'/api/bookings/bookings/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

    def test_overbooking(self):
        flight = Flight.objects.first()
        flight.seats_available = 2
        flight.save()
        data = {
            "flight": flight.id,
            "user": None,
            "booking_reference": "BKG-OVER789",
            "number_of_passengers": 3,
            "total_price": 450.00,
            "status": "confirmed",
            "contact_email": "guest@example.com",
            "contact_phone": "0987654321",
            "is_guest_booking": True,
            "passengers": [
                {"first_name": "Guest", "last_name": "One", "date_of_birth": "1980-01-01", 
                 "passport_number": "GO123456", "email_address": "guest1@example.com", 
                 "is_primary_passenger": True},
                {"first_name": "Guest", "last_name": "Two", "date_of_birth": "1982-02-02", 
                 "passport_number": "GT789012", "email_address": "guest2@example.com", 
                 "is_primary_passenger": False},
                {"first_name": "Guest", "last_name": "Three", "date_of_birth": "1983-03-03", 
                 "passport_number": "GT345678", "email_address": "guest3@example.com", 
                 "is_primary_passenger": False}
            ]
        }
        response = self.client.post('/api/bookings/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not enough seats available", str(response.data))

def test_invalid_passenger_count(self):
    flight = Flight.objects.first()
    data = {
        "flight": flight.id,
        "user": None,
        "booking_reference": "BKG-INV123",
        "number_of_passengers": 0,
        "total_price": 0.00,
        "status": "confirmed",
        "contact_email": "guest@example.com",
        "contact_phone": "0987654321",
        "is_guest_booking": True,
        "passengers": []
    }
    response = self.client.post('/api/bookings/bookings/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn("Number of passengers must be greater than zero", str(response.data))