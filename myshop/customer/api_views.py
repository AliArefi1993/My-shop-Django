from rest_framework import permissions, status
from rest_framework.response import Response
from users.models import CustomUser  # If used custom user model
from customer.models import Customer
from customer.serializers import UserSerializer, ProfileSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser


class CreateUserView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    model = CustomUser
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer


class CreateCustomerProfileView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    model = Customer
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = ProfileSerializer


class CustomerProfileUpdateDetailٰView(RetrieveUpdateAPIView):
    http_method_names = ['put', 'get']
    parser_classes = (MultiPartParser, FormParser)
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]

    def get_object(self):
        return get_object_or_404(Customer, custom_user_id=self.request.user.id)
