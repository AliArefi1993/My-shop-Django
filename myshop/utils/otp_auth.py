from django.conf import settings
from pyotp import TOTP
from typing import Any, Union, Optional
import hashlib


class VerifyTOTP(TOTP):
    """
    Handler for time-based OTP counters.
    """

    def __init__(self, s: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None,
                 issuer: Optional[str] = None, interval: int = 30) -> None:
        """
        :param s: secret in base32 format
        :param interval: the time interval in seconds for OTP. This defaults to 30.
        :param digits: number of integers in the OTP. Some apps expect this to be 6 digits, others support more.
        :param digest: digest function to use in the HMAC (expected to be sha1)
        :param name: account name
        :param issuer: issuer
        """

        super().__init__(s=s, digits=digits, digest=digest, name=name, issuer=issuer,
                         interval=int(settings.OTP_SETTINGS['VERIFY_TOTP']['INTERVAL']))


class LoginTOTP(TOTP):
    """
    Handler for time-based OTP counters.
    """

    def __init__(self, s: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None,
                 issuer: Optional[str] = None, interval: int = 30) -> None:
        """
        :param s: secret in base32 format
        :param interval: the time interval in seconds for OTP. This defaults to 30.
        :param digits: number of integers in the OTP. Some apps expect this to be 6 digits, others support more.
        :param digest: digest function to use in the HMAC (expected to be sha1)
        :param name: account name
        :param issuer: issuer
        """

        super().__init__(s=s, digits=digits, digest=digest, name=name, issuer=issuer,
                         interval=int(settings.OTP_SETTINGS['LOGIN_TOTP']['INTERVAL']))
