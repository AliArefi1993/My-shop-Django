from django.urls import path
from users.views.api_views import getPhoneNumberRegistered, getOTPLogin


app_name = 'users_api'
urlpatterns = [
    path('verify/<phone>/', getPhoneNumberRegistered.as_view(), name='verify_phone'),
    path('login/code/<phone>/', getOTPLogin.as_view(), name='login_otp'),

]
