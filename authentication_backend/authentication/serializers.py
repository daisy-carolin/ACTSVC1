from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number"]


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
