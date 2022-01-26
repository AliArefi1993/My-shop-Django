# Create your tasks here

import requests
import json
from django.core.cache import cache
from celery import shared_task
from django.conf import settings


@shared_task
def send_sms(phone, otp):
    sms_token = cache.get('sms_token')
    if not sms_token:
        url = "https://RestfulSms.com/api/Token"
        payload = json.dumps({
            "UserApiKey": settings.OTP_USER_API_KEY,
            "SecretKey": settings.OTP_SECRET_KEY
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        cache.set('sms_token', response.json()["TokenKey"], timeout=1800)

    url = "https://RestfulSms.com/api/VerificationCode"

    payload = json.dumps({
        "Code": otp,
        "MobileNumber": phone
    })
    headers = {
        'Content-Type': 'application/json',
        'x-sms-ir-secure-token': sms_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
