
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from order.serializers import OrderListSerializer, OrderPaySerializer, OrderAddSerializer,\
    OrderSubstractSerializer, OrderCreateSerializer
from order.models import Order
from rest_framework.parsers import FormParser, MultiPartParser


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
    http_method_names = ['patch', ]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderPaySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'message': 'OK'})


class OrderAddItemView(UpdateAPIView):
    http_method_names = ['patch', ]
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderAddSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class OrderSubstractItemView(UpdateAPIView):
    http_method_names = ['patch', ]
    queryset = Order.objects.filter(status="PEND")
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderSubstractSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class OrderCreateView(CreateAPIView):
    model = Order
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = OrderCreateSerializer
