from rest_framework.test import APITestCase
from rest_framework import status
from .models import Aircraft, Flight

class FlightTests(APITestCase):
    def setUp(self):
        # Create test data before each test
        aircraft = Aircraft.objects.create(
            model="Test Aircraft",
            capacity=5,
            registration_number="ZK-TEST",
            status="active"
        )
        Flight.objects.create(
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

    def test_get_flights(self):
        # Test retrieving list of flights
        response = self.client.get('/api/flights/flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['flight_number'], "TEST101")

    def test_create_flight(self):
        # Test creating a new flight
        aircraft = Aircraft.objects.first()
        data = {
            "flight_number": "TEST202",
            "origin": "New Origin",
            "destination": "New Destination",
            "departure_time": "2025-05-21T10:00:00Z",
            "arrival_time": "2025-05-21T12:00:00Z",
            "aircraft": aircraft.id,
            "capacity": 5,
            "seats_available": 5,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 2)