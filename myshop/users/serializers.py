from http.client import LENGTH_REQUIRED
from rest_framework import serializers


class OTPSerializer(serializers.Serializer):

    otp = serializers.CharField(max_length=6, min_length=6)
