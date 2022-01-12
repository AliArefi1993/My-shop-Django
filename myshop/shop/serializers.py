from django.db.models import fields
from rest_framework import serializers
from shop.models import Supplier, Type
from users.models import CustomUser  # If used custom user model
# Non-field imports, but public API
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser

User = CustomUser


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['name']


class SupplierListSerializer(serializers.ModelSerializer):
    type = TypeSerializer()

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'description',
                  'created_date', 'image', 'type', 'status']


class SupplierDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'description', 'country', 'state',
                  'city', 'address', 'post_code', 'custom_user',
                  'created_date', 'image', 'type', 'status']
