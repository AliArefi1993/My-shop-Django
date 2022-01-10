from rest_framework import serializers
from users.models import CustomUser  # If used custom user model


# class UserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     def create(self, validated_data):

#         user = CustomUser.objects.create_user(
#             phone=validated_data['phone'],
#             password=validated_data['password'],
#         )

#         return user

#     class Meta:
#         model = CustomUser
#         # Tuple of serialized model fields (see link [2])
#         fields = ("id", "phone", "password", )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'password',
                  'last_name', 'first_name', 'national_code', 'email']
