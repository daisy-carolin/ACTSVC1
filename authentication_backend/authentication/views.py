import random
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .email_verification import send_email_verification
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token

from .utils import MessageHandler
from .serializers import (
    AccountCreateSerializer,
    AccountSerializer,
    VerifyAccountSerializer,
)
from .email import send_otp_via_email_template
from .models import UserAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupView(APIView):
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            otp=random.randint(1000,9999)

            user = serializer.save(otp=otp)
            
            token = Token.objects.create(user=user)
            json = serializer.data
            json["token"] = token.key

            # send verification email
            current_site_url = get_current_site(request).domain
            send_email_verification(user, current_site_url, otp)

            # send OTP
            MessageHandler(
                phone_number=serializer.data.get('phone_number'),
                otp=otp
                ).send_otp_via_message()
            
            return Response(data={
                "message": "Account created. Please verify your email or phone numbe to proceed"
            }, 
            status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserEmail(APIView):
    def get(self, format=None, *args, **kwargs):
        user_id = kwargs.get("user_id", "")
        confirmation_token = kwargs.get("confirmation_token", "")
        try:
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                "Token is invalid or expired. Please request another confirmation email by signing in.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user.is_active = True
        user.otp_verified = True
        user.save()
        return Response("Email successfully confirmed", status=status.HTTP_200_OK)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")

            user = UserAccount.objects.filter(email=email).first()

            if not user:
                return Response(
                    {"message": "User does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if int(user.otp) == int(otp):
                user.is_active = True
                user.otp = None
                user.otp_verified = True
                user.save()
                login(request, user, backend='authentication.custom_auth_backend.PasswordlessAuthBackend')
                return Response({"message": "OTP verified."}, status=status.HTTP_200_OK)
            return Response(
                {"message": "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account_data = AccountSerializer(request.user).data
        return Response(
            {"message": "User data retrieved successfully.", "account": account_data},
            status=status.HTTP_200_OK,
        )
