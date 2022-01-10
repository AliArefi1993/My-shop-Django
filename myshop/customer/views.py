from django.shortcuts import render
from rest_framework import permissions
from users.models import CustomUser  # If used custom user model

from customer.serializers import UserSerializer
from rest_framework.generics import CreateAPIView


class CreateUserView(CreateAPIView):

    model = CustomUser
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer
