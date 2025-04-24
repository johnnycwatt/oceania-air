from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_of_birth', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}  # Password not returned in responses

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Hashes password
        return user