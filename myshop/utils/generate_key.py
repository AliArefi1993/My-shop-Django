import base64
from datetime import datetime
from django.conf import settings


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone, kind):
        return str(phone) + str(kind) + str(datetime.date(datetime.now())) + settings.OTP_SETTINGS['SECRET_KEY']

    @staticmethod
    def get_key(phone, kind):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(
            phone, kind).encode())
        return key
