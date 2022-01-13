
from drf_yasg.openapi import Response
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from customer.models import Customer
from shop.models import Type

from shop.serializers import TypeSerializer
from order.serializers import OrderListSerializer, OrderPaySerializer, OrderAddSerializer
from order.models import Order
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser


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


# class OrderCreateView(APIView):

#     model = Order
#     permission_classes = [
#         permissions.IsAuthenticated  # Or anon users can't register
#     ]
#     serializer_class = OrderCreateSerializer

#     # @swagger_auto_schema(responses=response_schema_dict)
#     def get(self, request, *args, **kwargs):
#         return Response({"foo": "bar"})
#         # return Response({}, status=status.HTTP_201_CREATED, headers=[])
#
    # def create(self, request, *args, **kwargs):
    #     return Response({'ali': 'qw'})

    # serializer = self.get_serializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # customer = Customer.objects.get(custom_user=request.user)

    # serializer.validated_data['customer'] = customer
    # serializer.validated_data['order_number'] = '1000'
    # self.perform_create(serializer)
    # headers = self.get_success_headers(serializer.data)
    # return Response({}, status=status.HTTP_201_CREATED, headers=[])

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     customer = Customer.objects.get(custom_user=request.user)
    #     print(customer)
    #     serializer.validated_data['customer'] = customer
    #     serializer.validated_data['order_number'] = '1000'
    #     print('10*************************')
    #     self.perform_create(serializer)
    #     print('10*************************')

    #     headers = self.get_success_headers(serializer.data)
    #     print('10*************************')
    #     print(serializer.data)
    #     print(status.HTTP_201_CREATED)
    #     print(headers)
    #     print(serializer.is_valid())
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
