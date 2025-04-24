from rest_framework import viewsets
from .models import Aircraft, Flight, Airport
from .serializers import AircraftSerializer, FlightSerializer, AirportSerializer
from django_filters.rest_framework import DjangoFilterBackend

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin__icao_code', 'destination__icao_code', 'departure_time']

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer