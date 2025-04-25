from rest_framework import serializers
from .models import Aircraft, Flight, Airport

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'icao_code', 'name', 'timezone']

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'model', 'capacity', 'registration_number', 'status']

class FlightSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(read_only=True) 
    origin = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    origin_id = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all(), source='origin', write_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(queryset=Airport.objects.all(), source='destination', write_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'origin', 'destination', 'departure_time',
            'arrival_time', 'aircraft', 'capacity', 'seats_available', 'price', 'status',
            'origin_id', 'destination_id'
        ]
    def validate(self, data):
        if data['origin'] == data['destination']:
            raise serializers.ValidationError("Origin and destination cannot be the same.")
        if data['departure_time'] >= data['arrival_time']:
            raise serializers.ValidationError("Arrival time must be after departure time.")
        if data['capacity'] <= 0:
            raise serializers.ValidationError("Capacity must be positive.")
        return data