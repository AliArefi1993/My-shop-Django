from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from utils.generate_key import generateKey
from utils.otp_auth import LoginTOTP
UserModel = get_user_model()


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        OTP = LoginTOTP(generateKey.get_key(username, 'login'))
        if OTP.verify(password):
            return user
