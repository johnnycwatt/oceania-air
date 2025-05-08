from rest_framework.test import APITestCase
from rest_framework import status
from .models import Aircraft, Flight, Airport
from django.utils import timezone

class FlightTests(APITestCase):
    def setUp(self):
        # Create test airports
        self.airport1 = Airport.objects.create(
            icao_code="TEST1", name="Test Airport 1", timezone="GMT+0"
        )
        self.airport2 = Airport.objects.create(
            icao_code="TEST2", name="Test Airport 2", timezone="GMT+0"
        )
        self.airport3 = Airport.objects.create(
            icao_code="TEST3", name="Test Airport 3", timezone="GMT+0"
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
            origin=self.airport1,  # Use Airport instance
            destination=self.airport2,  # Use Airport instance
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
            aircraft=self.aircraft,
            capacity=5,
            seats_available=5,
            price=150.00,
            status="scheduled"
        )

    def test_get_flights(self):
        response = self.client.get('/api/flights/flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['flight_number'], "TEST101")
        self.assertEqual(response.data[0]['origin']['id'], self.airport1.id)
        self.assertEqual(response.data[0]['destination']['id'], self.airport2.id)

    def test_flight_detail(self):
        response = self.client.get(f'/api/flights/flights/{self.flight.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flight_number'], "TEST101")
        self.assertEqual(response.data['origin']['id'], self.airport1.id)
        self.assertEqual(response.data['destination']['id'], self.airport2.id)

    def test_create_flight(self):
        data = {
            "flight_number": "TEST202",
            "origin_id": self.airport1.id,
            "destination_id": self.airport3.id,
            "departure_time": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            "arrival_time": (timezone.now() + timezone.timedelta(days=2, hours=2)).isoformat(),
            "aircraft_id": self.aircraft.id,
            "capacity": 5,
            "seats_available": 5,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 2)
        self.assertEqual(Flight.objects.get(flight_number="TEST202").origin, self.airport1)

    def test_create_flight_invalid_dates(self):
        data = {
            "flight_number": "TEST303",
            "origin_id": self.airport1.id,
            "destination_id": self.airport2.id,
            "departure_time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "arrival_time": (timezone.now() + timezone.timedelta(hours=23)).isoformat(),  # Before departure
            "aircraft_id": self.aircraft.id,
            "capacity": 5,
            "seats_available": 5,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Arrival time must be after departure time", str(response.data))

    def test_create_flight_invalid_capacity(self):
        data = {
            "flight_number": "TEST404",
            "origin_id": self.airport1.id,
            "destination_id": self.airport2.id,
            "departure_time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "arrival_time": (timezone.now() + timezone.timedelta(days=1, hours=2)).isoformat(),
            "aircraft_id": self.aircraft.id,
            "capacity": 0,  # Invalid
            "seats_available": 0,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Capacity must be positive", str(response.data))

    def test_create_flight_nonexistent_airport(self):
        data = {
            "flight_number": "TEST505",
            "origin_id": 9999,  # Non-existent ID
            "destination_id": self.airport2.id,
            "departure_time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "arrival_time": (timezone.now() + timezone.timedelta(days=1, hours=2)).isoformat(),
            "aircraft_id": self.aircraft.id,
            "capacity": 5,
            "seats_available": 5,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid pk", str(response.data))

    def test_create_flight_same_origin_destination(self):
        data = {
            "flight_number": "TEST606",
            "origin_id": self.airport1.id,
            "destination_id": self.airport1.id,  # Same as origin
            "departure_time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "arrival_time": (timezone.now() + timezone.timedelta(days=1, hours=2)).isoformat(),
            "aircraft_id": self.aircraft.id,
            "capacity": 5,
            "seats_available": 5,
            "price": 200.00,
            "status": "scheduled"
        }
        response = self.client.post('/api/flights/flights/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Origin and destination cannot be the same", str(response.data))