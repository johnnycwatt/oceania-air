from rest_framework.test import APITestCase
from rest_framework import status
from bookings.models import Booking, Passenger
from flights.models import Flight, Aircraft
from core.models import User  # Use custom User model

class BookingTests(APITestCase):
    def setUp(self):
        # Create test data before each test
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass",
            date_of_birth="1990-01-01",
            phone_number="1234567890"
        )
        aircraft = Aircraft.objects.create(
            model="Test Aircraft",
            capacity=5,
            registration_number="ZK-TEST",
            status="active"
        )
        flight = Flight.objects.create(
            flight_number="TEST101",
            origin="Test Origin",
            destination="Test Destination",
            departure_time="2025-05-20T10:00:00Z",
            arrival_time="2025-05-20T12:00:00Z",
            aircraft=aircraft,
            capacity=5,
            seats_available=5,
            price=150.00,
            status="scheduled"
        )
        booking = Booking.objects.create(
            user=user,
            flight=flight,
            booking_reference="BKG-TEST123",
            number_of_passengers=1,
            total_price=150.00,
            status="confirmed",
            contact_email="test@example.com",
            contact_phone="1234567890",
            is_guest_booking=False
        )
        Passenger.objects.create(
            booking=booking,
            first_name="Test",
            last_name="Passenger",
            date_of_birth="1990-01-01",
            passport_number="TP123456",
            email_address="test@example.com",
            is_primary_passenger=True
        )

    def test_get_bookings(self):
        # Test retrieving list of bookings
        response = self.client.get('/api/bookings/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['booking_reference'], "BKG-TEST123")

    def test_create_booking(self):
        # Test creating a new guest booking with passengers
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
        # Test updating a booking's status
        booking = Booking.objects.first()
        data = {"status": "cancelled"}
        response = self.client.patch(f'/api/bookings/bookings/{booking.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")

    def test_delete_booking(self):
        # Test deleting a booking
        booking = Booking.objects