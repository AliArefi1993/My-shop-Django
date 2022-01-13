from rest_framework import permissions, status
from rest_framework.response import Response
from users.models import CustomUser  # If used custom user model
from customer.models import Customer
from customer.serializers import UserSerializer, ProfileSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser


class CreateUserView(CreateAPIView):

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['custom_user'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerProfileUpdateDetailٰView(RetrieveUpdateAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    model = Customer
    queryset = Customer.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
