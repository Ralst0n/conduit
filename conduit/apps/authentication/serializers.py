from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
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

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        return user email, username & token if user exists
        """
        # validate that the username and password are provided
        # & exist in the database
        email = data.get('email', None)
        password = data.get('password', None)

        #raise exceptions if not provided
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in'
            )

        #authenticate model is imported from and provided by django
        ###it checks for a user matching the provided email/pass combo
        user = authenticate(username=email, password=password)

        #authenticate returns None if combination not found
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        #make sure user hasn't deactivated the account/been banned
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )

        #return validated data if everything checks out
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # passwords between 8 - 128 characters
    # cause it is django default
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        # use 'read_only_fields' option rather than 'read_only=True'
        # a la password fields above, when nothing else about field
        # needs to be specified
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with 'setattr' unlike other fields
        # Django provides function that handles hashing & salting passwords
        # so we must remove password field from 'validated_data' first
        password = validated_data.pop('password', None)

        for(key, value) in validated_data.items():
            # set the validated_data items on the current 'User'
            setattr(instance, key, value)

        if password is not None:
            # '.set_password()' handles all of the security stuff
            instance.set_password(password)

        # After everything has been updated save the model
        instance.save()

        return instance
