from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from shop.models import Supplier, Type
from shop.serializers import SupplierListSerializer, TypeSerializer
from rest_framework import permissions, status
from shop.filter import SupplierListFilter
from rest_framework import generics


# class SupplierListView2(ListAPIView):
#     model = Supplier
#     permission_classes = [
#         permissions.IsAuthenticated  # Or anon users can't register
#     ]
#     serializer_class = SupplierListSerializer
#     queryset = Supplier.available.all()
#     filterset_class = SupplierListFilter


class SupplierListView(generics.ListAPIView):
    filterset_class = SupplierListFilter
    queryset = Supplier.available.filter(status='CONF')
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = SupplierListSerializer


class SupplierTypeListView(generics.ListAPIView):
    queryset = Type.objects.all()
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = TypeSerializer
