from rest_framework import serializers
from .models import Booking, Passenger, BookingPassenger
from flights.models import Flight

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'passport_number', 'email_address']

class BookingPassengerSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer()
    is_primary_passenger = serializers.BooleanField()

    class Meta:
        model = BookingPassenger
        fields = ['passenger', 'is_primary_passenger']

class BookingSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())
    passengers = BookingPassengerSerializer(many=True, source='bookingpassenger_set')

    class Meta:
        model = Booking
        fields = [
            'id', 'flight', 'booking_reference', 'total_price', 'status',
            'contact_email', 'contact_phone', 'passengers'
        ]

    def validate(self, data):
        # For updates, use instance.flight if 'flight' not in data; for creation, require it
        flight = data.get('flight', self.instance.flight if self.instance else None)
        if not flight:
            raise serializers.ValidationError("Flight is required.")

        # Only validate passengers if provided in data
        passengers_data = data.get('bookingpassenger_set', None)
        if passengers_data is not None:
            num_passengers = len(passengers_data)
            if num_passengers > flight.seats_available:
                raise serializers.ValidationError("Not enough seats available.")
            if num_passengers <= 0:
                raise serializers.ValidationError("At least one passenger is required.")
        elif not self.instance:
            raise serializers.ValidationError("Passengers are required for new bookings.")
        return data

    def create(self, validated_data):
        passengers_data = validated_data.pop('bookingpassenger_set', [])
        booking = Booking.objects.create(**validated_data)
        total_price = 0
        for passenger_data in passengers_data:
            passenger_info = passenger_data['passenger']
            is_primary = passenger_data['is_primary_passenger']
            passenger, _ = Passenger.objects.get_or_create(
                email_address=passenger_info['email_address'],
                defaults={
                    'first_name': passenger_info['first_name'],
                    'last_name': passenger_info['last_name'],
                    'date_of_birth': passenger_info['date_of_birth'],
                    'passport_number': passenger_info.get('passport_number', '')
                }
            )
            BookingPassenger.objects.create(
                booking=booking,
                passenger=passenger,
                is_primary_passenger=is_primary
            )
            total_price += booking.flight.price
        booking.total_price = total_price
        booking.save()
        booking.flight.seats_available -= len(passengers_data)
        booking.flight.save()
        return booking

    def update(self, instance, validated_data):
        passengers_data = validated_data.pop('bookingpassenger_set', None)
        instance = super().update(instance, validated_data)
        if passengers_data is not None:
            instance.bookingpassenger_set.all().delete()
            total_price = 0
            for passenger_data in passengers_data:
                passenger_info = passenger_data['passenger']
                is_primary = passenger_data['is_primary_passenger']
                passenger, _ = Passenger.objects.get_or_create(
                    email_address=passenger_info['email_address'],
                    defaults={
                        'first_name': passenger_info['first_name'],
                        'last_name': passenger_info['last_name'],
                        'date_of_birth': passenger_info['date_of_birth'],
                        'passport_number': passenger_info.get('passport_number', '')
                    }
                )
                BookingPassenger.objects.create(
                    booking=instance,
                    passenger=passenger,
                    is_primary_passenger=is_primary
                )
                total_price += instance.flight.price
            instance.total_price = total_price
            instance.save()
        return instance