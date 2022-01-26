from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser
from utils.generate_key import generateKey
from utils.otp_auth import VerifyTOTP, LoginTOTP
from drf_yasg.utils import swagger_auto_schema
from users.serializers import OTPSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from users.tasks import send_sms


class VerifyPhoneNumberView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, phone):
        try:
            Mobile = CustomUser.objects.get(
                phone=phone)
            if Mobile.phone_is_submitted == True:
                return Response({"message": "Your number already has been submitted"}, status=400)
        except ObjectDoesNotExist:
            return Response({"message": "Your number hase't been registered yet."}, status=404)
        OTP = VerifyTOTP(generateKey.get_key(phone, 'verify'))
        otp = OTP.now()
        send_sms.delay(phone, otp)
        return Response({"OTP": otp}, status=200)

    # This Method verifies the OTP
    @swagger_auto_schema(operation_description="description", request_body=OTPSerializer)
    def post(self, request, phone):
        try:
            Mobile = CustomUser.objects.get(phone=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call
        OTP = VerifyTOTP(generateKey.get_key(phone, 'verify'))
        if OTP.verify(request.data["otp"]):
            Mobile.phone_is_submitted = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=401)


class OTPLoginView(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = CustomUser.objects.get(
                phone=phone)
            if Mobile.phone_is_submitted == False:
                return Response({"message": "Your need to submit your phone number first"}, status=401)
        except ObjectDoesNotExist:
            return Response({"message": "Your haven't registered with this phone number yet."}, status=404)
        OTP = LoginTOTP(generateKey.get_key(phone, 'login'))
        otp = OTP.now()
        send_sms.delay(phone, otp)
        return Response({"OTP": otp}, status=200)
