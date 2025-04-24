from rest_framework import serializers
from .models import Aircraft, Flight

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'model', 'capacity', 'registration_number', 'status']

class FlightSerializer(serializers.ModelSerializer):
    aircraft = serializers.PrimaryKeyRelatedField(queryset=Aircraft.objects.all())

    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'origin', 'destination', 'departure_time',
            'arrival_time', 'aircraft', 'capacity', 'seats_available', 'price', 'status'
        ]

    def validate(self, data):
        if data['departure_time'] >= data['arrival_time']:
            raise serializers.ValidationError("Arrival time must be after departure time.")
        if data['capacity'] <= 0:
            raise serializers.ValidationError("Capacity must be positive.")
        return data