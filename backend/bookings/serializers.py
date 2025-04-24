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
        passengers_data = validated_data.pop('passengers', [])  # Remove passengers first
        validated_data['total_price'] = validated_data['flight'].price * validated_data['number_of_passengers']
        booking = Booking.objects.create(**validated_data)  # Now validated_data has only Booking fields
        for passenger_data in passengers_data:
            Passenger.objects.create(booking=booking, **passenger_data)
        booking.flight.seats_available -= booking.number_of_passengers
        booking.flight.save()
        return booking

    def update(self, instance, validated_data):
        passengers_data = validated_data.pop('passengers', None)
        instance = super().update(instance, validated_data)
        if passengers_data is not None:
            instance.passengers.all().delete()
            for passenger_data in passengers_data:
                Passenger.objects.create(booking=instance, **passenger_data)
        return instance
    
    def validate(self, data):
        flight = data.get('flight', self.instance.flight if self.instance else None)
        if flight:
            num_passengers = data.get('number_of_passengers', 
                                    self.instance.number_of_passengers if self.instance else 0)
            if num_passengers > flight.seats_available:
                raise serializers.ValidationError("Not enough seats available.")
            if num_passengers <= 0:
                raise serializers.ValidationError("Number of passengers must be greater than zero.")
        return data