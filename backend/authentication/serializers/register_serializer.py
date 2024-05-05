from rest_framework import serializers
from authentication.models import User
import re


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name', 'phone_number', 'password']

    def create(self, validated_data):
        # Extract the password from the validated data
        password = validated_data.pop('password', None)

        # Create a new user instance
        user = User(**validated_data)

        # Set and encrypt the password if provided
        if password:
            user.set_password(password)

        # Save the user
        user.save()
        return user
