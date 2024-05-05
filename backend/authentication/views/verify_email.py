
from rest_framework import serializers,  status, generics

from utils.response import Response
from authentication.models import User
import jwt
from django.conf import settings


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)


class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        user_data = self.serializer_class(data=request.data)
        if user_data.is_valid():
            token = user_data.validated_data['token']
            print("token", token)
            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=['HS256'])
                print("payload", payload)
                user = User.objects.get(id=payload['user_id'])
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    return Response({'data': 'Email successfully activated'}, status=status.HTTP_200_OK)
                else:
                    return Response({'data': 'Email is already verified'}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError as e:
                return Response({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError as e:
                # print("JWT Decode Error:", str(e))
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist as e:
                print("JWT Decode Error:", str(e))
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)
