from rest_framework import viewsets
from .models import Aircraft, Flight, Airport
from .serializers import AircraftSerializer, FlightSerializer, AirportSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, IsoDateTimeFilter, CharFilter

class FlightFilter(FilterSet):
    origin__icao_code = CharFilter(field_name='origin__icao_code')
    destination__icao_code = CharFilter(field_name='destination__icao_code')
    departure_time__gte = IsoDateTimeFilter(field_name='departure_time', lookup_expr='gte')
    departure_time__lt = IsoDateTimeFilter(field_name='departure_time', lookup_expr='lt')

    class Meta:
        model = Flight
        fields = ['origin__icao_code', 'destination__icao_code', 'departure_time__gte', 'departure_time__lt']

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer