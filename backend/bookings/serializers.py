from rest_framework import serializers
from .models import Booking, Passenger
from flights.models import Flight
from core.models import User

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth',
            'passport_number', 'email_address', 'is_primary_passenger'
        ]

class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'flight', 'booking_reference', 'number_of_passengers',
            'total_price', 'status', 'contact_email', 'contact_phone',
            'is_guest_booking', 'passengers'
        ]

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        booking = Booking.objects.create(**validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(booking=booking, **passenger_data)
        return booking

    def update(self, instance, validated_data):
        passengers_data = validated_data.pop('passengers', None)
        instance = super().update(instance, validated_data)
        if passengers_data is not None:  # Only update passengers if provided
            instance.passengers.all().delete()  # Replace existing passengers
            for passenger_data in passengers_data:
                Passenger.objects.create(booking=instance, **passenger_data)
        return instance