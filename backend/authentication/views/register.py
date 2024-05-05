from utils.response import Response
import json
import os
from utils.email_templates import AWSEmailTemplateManager
from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import RegisterSerializer
from dotenv import load_dotenv
load_dotenv()


VERIFY_URL = os.environ.get('VERIFY_URL')
SOURCE = os.environ.get('SOURCE')
CURRENT_SITE = f'{VERIFY_URL}/email-verify'


def send_verification_email(email, name, link):
    tem_mgr = AWSEmailTemplateManager()
    source = SOURCE
    destination = {
        'ToAddresses': [str(email)]
    }

    template_data = {
        'name': name,
        'link': link
    }
    template_data_json = json.dumps(template_data)
    print("template data", template_data_json)
    template_name = "AccountActivationTemplate"
    tem_mgr.send_templated_email(
        source, destination, template_name, template_data_json)
    return True


class RegisterView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class=RegisterSerializer

    def post(self, request):
        data = request.data
        email = data['email']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        name = f'{first_name} {last_name}'
        existing_verified_user = get_user_model().objects.get(
            email=email, is_verified=True)
        if existing_verified_user:
            return Response({
                "error": "User already exists and is verified. Please login or click on 'forgot password' to reset your password."
            }, status=status.HTTP_400_BAD_REQUEST)

        existing_unverified_user = get_user_model().objects.get(
            email=email, is_verified=False)
        if existing_unverified_user:
            token = RefreshToken.for_user(
                existing_unverified_user).access_token
            link = CURRENT_SITE + "?token=" + str(token)

            send_verification_email(email, name, link)

            return Response({
                "error": "An activation link has been sent to your email."
            }, status=status.HTTP_201_CREATED)

        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user).access_token
                link = CURRENT_SITE + "?token=" + str(token)
                send_verification_email(
                    email, name, link)
                return Response({"message": "Account created, please check your email for a verification link"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Please enter valid input"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
