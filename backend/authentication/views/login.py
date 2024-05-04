from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_verified:

            token['first_name'] = user.first_name
            token['last_name'] = user.first_name
            token['middle_name'] = user.middle_name
            token['email'] = user.email
            token['practice_name'] = user.practice_name
            token['is_verified'] = user.is_verified
            token['is_active'] = user.is_active
            token['phone_number'] = user.phone_number
            return token
        else:
            raise PermissionDenied("User not verified")

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        return super().validate(attrs)


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer
