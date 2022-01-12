from rest_framework import serializers
from users.models import CustomUser  # If used custom user model
# Non-field imports, but public API
from rest_framework.fields import ReadOnlyField, empty
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from customer.models import Customer, ImageTest
from rest_framework.serializers import Serializer, raise_errors_on_nested_writes
from rest_framework.utils import model_meta
import traceback

User = CustomUser


class ImageTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTest
        fields = ['name', 'image']


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='custom_user.image')

    class Meta:
        model = Customer
        fields = ["customer_username", "country", "state",
                  "city", "address", "post_code", "custom_user", "image"]
        related_fields = ["custom_user"]
        extra_kwargs = {
            'custom_user': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # related object available
        try:
            # Handle related objects
            for related_obj_name in self.Meta.related_fields:

                # Validated data will show the nested structure
                data = validated_data.pop(related_obj_name)
                related_instance = getattr(instance, related_obj_name)

                # Same as default update implementation
                for attr_name, value in data.items():
                    setattr(related_instance, attr_name, value)
                related_instance.save()
        except:
            pass
        return super(ProfileSerializer, self).update(instance, validated_data)
    # Default `create` and `update` behavior...


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'password', 'password2',
                  'last_name', 'first_name', 'national_code', 'email']

        extra_kwargs = {
            'password': {'write_only': True},
            'national_code': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data['phone'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            national_code=validated_data['national_code'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
