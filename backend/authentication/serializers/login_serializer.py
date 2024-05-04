from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

