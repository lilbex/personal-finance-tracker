from rest_framework import serializers,  status, views
from rest_framework.response import Response
from authentication.models import User
import jwt
from django.conf import settings

class SetNewPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    password = serializers.CharField(max_length=68, min_length=8)

    class Meta:
        model = User
        fields = ['token', 'password']


class ResetPassword(views.APIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        user_data = request.data
        token = user_data.get('token', '')
        password = user_data.get('password', '')
        try:
            # payload = jwt.decode(token, settings.SECRET_KEY)
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])

            user = User.objects.get(id=payload['user_id'])
            user.set_password(password)
            user.save()
            return Response({'email': 'Password successfully reset'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': str(identifier)}, status=status.HTTP_400_BAD_REQUEST)
