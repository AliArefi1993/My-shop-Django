from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from users.models import CustomUser  # If used custom user model
from customer.models import Customer, ImageTest
from customer.serializers import UserSerializer, ProfileSerializer, ImageTestSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser


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

    # def get_queryset(self):
    #     if self.request.method == 'GET':
    #         Customer.objects.all()
    #     else:
    #         return Customer.objects.filter()

    # def update(self, request, *args, **kwargs):

    #     partial = kwargs.pop('partial', False)
    #     # my_user = request.user

    #     # try:
    #     #     my_user.image = request.data['image']
    #     #     my_user.save()
    #     # except:
    #     #     if partial == False:
    #     #         return Response({"image": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)


class UploadImageTestView(CreateAPIView):

    model = ImageTest
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = ImageTestSerializer
