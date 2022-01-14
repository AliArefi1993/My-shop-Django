from rest_framework import serializers
from rest_framework.utils import model_meta
from users.models import CustomUser  # If used custom user model
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from customer.models import Customer
import traceback

User = CustomUser


class ProfileSerializer(serializers.ModelSerializer):

    # # Create a custom method field
    # current_user = serializers.SerializerMethodField('_user')

    # # Use this method for the custom field
    # def _user(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return request.user

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

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        serializers.raise_errors_on_nested_writes(
            'create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        validated_data['custom_user'] = self.context['request'].user
        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


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
