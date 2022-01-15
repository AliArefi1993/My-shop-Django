from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.utils import model_meta
from customer.models import Customer
from order.models import OrderItem
from shop.models import Product
from order.models import Order
from users.models import CustomUser
import traceback

User = CustomUser


class OrderCreateSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source='customer.customer_username', read_only=True)
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Product.objects.all(), source='items')

    class Meta:
        model = Order
        fields = ['id', 'customer_username', 'order_number',
                  'order_date', 'total_price', 'items', 'status', 'item_ids']
        extra_kwargs = {
            'id': {'read_only': True},
            'customer_username': {'read_only': True},
            'order_number': {'read_only': True},
            'order_date': {'read_only': True},
            'total_price': {'read_only': True},
            # 'items': {'read_only': True},
            'status': {'read_only': True},
        }

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
        try:
            validated_data['customer'] = Customer.objects.get(
                custom_user=self.context['request'].user)
        except:
            raise NotFound(**{'detail': 'customer profile not found.'})

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
        product = self.validated_data['items'][0]
        if product.supplier.status != 'CONF' or product.quantity == 0:
            raise NotFound(**{'detail': 'product not available.'})

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        order_id = instance.pk

        current_order_item = OrderItem.objects.get(
            product=product, order=order_id)

        current_order_item.price = product.unit_price
        current_order_item.quantity = 1
        current_order_item.save()
        product.quantity = product.quantity - 1
        product.save()
        instance.total_price += product.unit_price
        instance.save()
        return instance


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderPaySerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source='customer.customer_username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_username', 'order_number',
                  'order_date', 'total_price', 'items', 'status']
        extra_kwargs = {
            'id': {'read_only': True},
            'customer_username': {'read_only': True},
            'order_number': {'read_only': True},
            'order_date': {'read_only': True},
            'total_price': {'read_only': True},
            'items': {'read_only': True},
            'status': {'read_only': True},
        }

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes(
            'update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        validated_data['status'] = 'PAID'
        OrderItem.objects.filter(order=self.data['id']).exclude(
            quantity=0).update(status='PAID')

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class OrderAddSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source='customer.customer_username', read_only=True)

    item_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Product.objects.all(), source='items')

    class Meta:
        model = Order
        fields = ['id', 'customer_username', 'order_number',
                  'order_date', 'total_price', 'items', 'status', 'item_ids']
        extra_kwargs = {
            'id': {'read_only': True},
            'customer_username': {'read_only': True},
            'order_number': {'read_only': True},
            'order_date': {'read_only': True},
            'total_price': {'read_only': True},
            # 'items': {'read_only': True},
            'status': {'read_only': True},
        }

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes(
            'update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        product = self.validated_data['items'][0]
        if product.supplier.status != 'CONF' or product.quantity == 0:
            raise NotFound(**{'detail': 'product not available.'})

        m2m_fields = []

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        order_id = self.data['id']

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.add(value[0])
        if product.supplier.status != 'CONF':
            raise NotFound
        current_order_item = OrderItem.objects.get(
            product=product, order=order_id)
        current_order_item.quantity += 1
        current_order_item.price += product.unit_price

        instance.total_price += product.unit_price
        instance.save()
        current_order_item.save()
        product.quantity = product.quantity - 1
        product.save()
        self.is_valid()
        current_order_item.save()

        return instance


class OrderSubstractSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(
        source='customer.customer_username', read_only=True)

    item_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Product.objects.all(), source='items')

    class Meta:
        model = Order
        fields = ['id', 'customer_username', 'order_number',
                  'order_date', 'total_price', 'items', 'status', 'item_ids']
        extra_kwargs = {
            'id': {'read_only': True},
            'customer_username': {'read_only': True},
            'order_number': {'read_only': True},
            'order_date': {'read_only': True},
            'total_price': {'read_only': True},
            # 'items': {'read_only': True},
            'status': {'read_only': True},
        }

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes(
            'update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        order_id = self.data['id']

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        try:
            product = self.validated_data['items'][0]
            if product.supplier.status != 'CONF':
                raise NotFound
            current_order_item = OrderItem.objects.get(
                product=product, order=order_id)
        except:
            raise NotFound
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.add(value[0])
        product = self.validated_data['items'][0]
        current_order_item = OrderItem.objects.get(
            product=product, order=order_id)
        if current_order_item.quantity > 0:
            current_order_item.price -= product.unit_price
            current_order_item.quantity -= 1
            instance.total_price -= product.unit_price
            if current_order_item.quantity == 0:
                current_order_item.status = 'CANC'
                if instance.total_price == 0:
                    instance.status = 'CANC'
            product.quantity = product.quantity + 1
            product.save()
            current_order_item.save()
            instance.save()
        else:
            raise NotFound

        return instance
