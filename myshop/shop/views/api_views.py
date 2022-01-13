
from shop.models import Supplier, Type, Product
from shop.serializers import SupplierListSerializer, TypeSerializer, ProductListSerializer
from rest_framework import permissions
from shop.filter import SupplierListFilter, SupplierProductListFilter
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


class SupplierProductListView(generics.ListAPIView):
    model = Product
    filterset_class = SupplierProductListFilter
    queryset = Product.objects.exclude(quantity=0)
    permission_classes = [
        permissions.IsAuthenticated  # Or anon users can't register
    ]
    serializer_class = ProductListSerializer

    def get(self, request, *args, **kwargs):
        self.supplier_slug = kwargs['slug']
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        self.queryset = self.model.objects.filter(
            supplier__slug=self.supplier_slug).exclude(quantity=0)
        return super().get_queryset(*args, **kwargs)
