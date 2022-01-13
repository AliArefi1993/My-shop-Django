from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from shop.models import Product
from order.models import Order
from users.models import CustomUser

User = CustomUser


class OrderListSerializer(serializers.ModelSerializer):
    # product_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = '__all__'
    #     # extra_kwargs = {
    #     #     'product_id': {'read_only': True},
    #     # }
