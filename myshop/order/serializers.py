from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.utils import model_meta
from order.models import OrderItem
from shop.models import Product
from order.models import Order
from users.models import CustomUser
import traceback

User = CustomUser

# product_id = serializers.IntegerField()
#     # extra_kwargs = {
#     #     'product_id': {'read_only': True},
#     # }


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
        product_id = self.validated_data['items'][0]
        current_order_item = OrderItem.objects.get(
            product=product_id, order=order_id)
        if current_order_item.quantity:
            current_order_item.quantity += 1
        else:
            current_order_item.quantity = 1
        current_order_item.save()
        return instance
