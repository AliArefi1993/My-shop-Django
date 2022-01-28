from django.urls import path
from users.views.api_views import VerifyPhoneNumberView, OTPLoginView


app_name = 'users_api'
urlpatterns = [
    path('verify/<phone>/', VerifyPhoneNumberView.as_view(), name='verify_phone'),
    path('login/code/<phone>/', OTPLoginView.as_view(), name='login_otp'),

]
