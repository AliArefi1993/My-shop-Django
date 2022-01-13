
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import permissions

from order.serializers import OrderListSerializer, OrderPaySerializer, OrderAddSerializer,\
    OrderSubstractSerializer, OrderCreateSerializer
from order.models import Order
from drf_yasg import openapi
from rest_framework.parsers import FormParser, MultiPartParser


response_schema_dict = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "200_key1": "200_value_1",
                "200_key2": "200_value_2",
            }
        }
    ),
    "205": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}


class OrderListPendView(ListAPIView):
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderListSerializer


class OrderListPreviousView(ListAPIView):
    queryset = Order.objects.exclude(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderListSerializer


class OrderPayView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderPaySerializer


class OrderAddItemView(UpdateAPIView):
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderAddSerializer


class OrderSubstractItemView(UpdateAPIView):
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderSubstractSerializer


class OrderCreateView(CreateAPIView):

    model = Order
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderCreateSerializer
