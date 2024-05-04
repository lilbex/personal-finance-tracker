from rest_framework import serializers
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json
from utils.email_templates import AWSEmailTemplateManager
from dotenv import load_dotenv
import os

load_dotenv()
SOURCE = os.environ.get('SOURCE')

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class ForgotPasswordRequestView(generics.GenericAPIView):
    serializer_class = ForgotPasswordRequestSerializer

    def post(self, request):

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = RefreshToken.for_user(user).access_token
            current_site = settings.VERIFY_URL + 'forgot-password'
            link = current_site +"?token="+str(token)
            tem_mgr = AWSEmailTemplateManager()
            source = SOURCE
            destination = {
                'ToAddresses': [str(email)]
            }

            template_data = {
                'name': user.first_name,
                'link': link
            }
            template_data_json = json.dumps(template_data)
         
            template_name = "AccountActivationTemplate"
            tem_mgr.send_templated_email(
                source, destination, template_name, template_data_json)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
                return Response({'error': 'Email does not exist'}, status=status.HTTP_400_BAD_REQUEST)