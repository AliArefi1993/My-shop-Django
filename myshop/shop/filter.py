import django_filters

from shop.models import Supplier


class SupplierListFilter(django_filters.FilterSet):
    type__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['type']
