from django.urls import path
from customer.api_views import CreateUserView, CreateCustomerProfileView,\
    CustomerProfileUpdateDetailٰView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'customer_api'
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',
         CreateUserView.as_view(), name='register'),
    path('profile/',
         CreateCustomerProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>',
         CustomerProfileUpdateDetailٰView.as_view(), name='profile'),

]
