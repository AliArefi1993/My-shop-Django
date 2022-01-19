from django.shortcuts import render

from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
import base64


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key (1234554321)"


class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):

        try:
            Mobile = CustomUser.objects.get(
                phone=phone)
            if Mobile.phone_is_submitted == True:
                return Response({"message": "Your number already has been submitted"}, status=400)
        except ObjectDoesNotExist:
            return Response({"message": "Your number hase't been registered yet."}, status=400)
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Key is generated
        # HOTP Model for OTP is created    TOTP
        OTP = pyotp.TOTP(key, interval=90)

        return Response({"OTP": OTP.now()}, status=200)

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = CustomUser.objects.get(phone=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key, interval=90)  # TOTP Model
        if OTP.verify(request.data["otp"]):
            Mobile.phone_is_submitted = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)


class getOTPLogin(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):

        try:
            Mobile = CustomUser.objects.get(
                phone=phone)
            if Mobile.phone_is_submitted == False:
                return Response({"message": "Your need to submit your phone number first"}, status=400)
        except ObjectDoesNotExist:
            return Response({"message": "Your haven't registered with this phone number yet."}, status=400)
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone).encode())  # Key is generated
        # HOTP Model for OTP is created    TOTP
        OTP = pyotp.TOTP(key, interval=90)

        return Response({"OTP": OTP.now()}, status=200)
