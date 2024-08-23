
from rest_framework import serializers
from .models import data
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


       # Define the validate method to handle custom validation
    def validate(self, attrs):
        # Extract the username and password from the validated data
        username = attrs.get('username')
        password = attrs.get('password')

        # Check if both username and password are provided
        if username and password:
            # Authenticate the user with the provided credentials
            user = authenticate(username=username, password=password)
            if user:
                # If authentication is successful, add the user to the validated data
                attrs['user'] = user
            else:
                # Raise a validation error if authentication fails
                 raise serializers.ValidationError('Must include "username" and "password".')
        else:
            # Raise a validation error if username or password is missing
            raise serializers.ValidationError('Must include "username" and "password".')

        # Return the validated data
        return attrs
    
