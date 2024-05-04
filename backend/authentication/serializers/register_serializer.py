from rest_framework import serializers
from authentication.models import User
import re


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email',
                    'first_name',
                    'last_name',
                    'phone_number',]

