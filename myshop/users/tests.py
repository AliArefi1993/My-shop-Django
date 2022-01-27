from time import sleep
from django.urls.base import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase
from users.models import CustomUser
from django.conf import settings

User = CustomUser


class TestVerifyOTPPhone(APITestCase):
    "Test for getting list of pended orders"

    def setUp(self):
        self.user1 = mommy.make(User, phone_is_submitted=False)
        self.user2 = mommy.make(User, phone_is_submitted=True)
        self.user3 = mommy.make(User, phone_is_submitted=False)

    def test_get_verify_otp_code(self):
        url = reverse('users_api:verify_phone', args=[self.user1.phone])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght of OTP
        self.assertEqual(len(resp.data['OTP']), 6)

        # check the response to a user who already has been verified
        url = reverse('users_api:verify_phone', args=[self.user2.phone])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 400)

        # check the response to a phone who has'nt been registered yet
        url = reverse('users_api:verify_phone', args=['+989301605689'])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 404)

    def test_post_verify_otp_cod(self):
        url = reverse('users_api:verify_phone', args=[self.user1.phone])
        resp = self.client.get(url)
        otp = resp.data['OTP']
        url = reverse('users_api:verify_phone', args=[self.user1.phone])
        resp = self.client.post(url, {'otp': otp})

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response to another user with otp
        url = reverse('users_api:verify_phone', args=[self.user2.phone])
        resp = self.client.post(url, {'otp': otp})
        self.assertEqual(resp.status_code, 400)

        #   check the response after lost of code validity
        url = reverse('users_api:verify_phone', args=[self.user3.phone])
        resp = self.client.get(url)
        otp = resp.data['OTP']
        url = reverse('users_api:verify_phone', args=[self.user3.phone])
        sleep(int(settings.OTP_SETTINGS['VERIFY_TOTP']['INTERVAL']))
        resp = self.client.post(url, {'otp': otp})

        #   check the response status
        self.assertEqual(resp.status_code, 400)


class TestLoginOTPPhone(APITestCase):
    "Test for getting list of pended orders"

    def setUp(self):
        self.user1 = mommy.make(User, phone_is_submitted=False)
        self.user2 = mommy.make(User, phone_is_submitted=True)
        self.user3 = mommy.make(User, phone_is_submitted=False)

    def test_get_verify_otp_code(self):
        url = reverse('users_api:login_otp', args=[self.user2.phone])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response lenght of OTP
        self.assertEqual(len(resp.data['OTP']), 6)

        # check the response to a user who already has not been verified
        url = reverse('users_api:login_otp', args=[self.user1.phone])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 401)

        # check the response to a phone who has'nt been registered yet
        url = reverse('users_api:login_otp', args=['+989301605689'])
        resp = self.client.get(url)

        #   check the response status
        self.assertEqual(resp.status_code, 404)

    def test_post_login_otp_cod(self):
        url = reverse('users_api:login_otp', args=[self.user2.phone])
        resp = self.client.get(url)
        otp = resp.data['OTP']
        url = reverse('customer_api:token_obtain_pair')
        login_data = {'password': otp, 'phone': self.user2.phone}
        resp = self.client.post(url, login_data)

        #   check the response status
        self.assertEqual(resp.status_code, 200)

        #   check the response to another user with otp
        url = reverse('customer_api:token_obtain_pair')
        login_data = {'password': otp, 'phone': self.user1.phone}
        resp = self.client.post(url, login_data)
        self.assertEqual(resp.status_code, 401)

        #   check the response after lost of code validity
        url = reverse('users_api:login_otp', args=[self.user2.phone])
        resp = self.client.get(url)
        otp = resp.data['OTP']
        url = reverse('customer_api:token_obtain_pair')
        login_data = {'password': otp, 'phone': self.user2.phone}
        sleep(int(settings.OTP_SETTINGS['LOGIN_TOTP']['INTERVAL']))
        resp = self.client.post(url, login_data)

        #   check the response status
        self.assertEqual(resp.status_code, 401)
