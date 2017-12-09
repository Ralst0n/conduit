from rest_framework import serializers

from .models import User

class RegistrationSerializer(serializer.ModelSerializer):
    """Serializers, registration requests and creates a new user"""

    # Ensure passwords are 8-128 and can't be read by client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The cli
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        #list all fields that could be included in a
        #request OR response including those above
        fields = ['email', 'username', 'password',  'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
