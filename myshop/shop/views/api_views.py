from rest_framework.generics import ListAPIView
from shop.models import Supplier
from shop.serializers import SupplierListSerializer
from rest_framework import permissions


class SupplierListView(ListAPIView):
    model = Supplier
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = SupplierListSerializer
    queryset = Supplier.available.all()
