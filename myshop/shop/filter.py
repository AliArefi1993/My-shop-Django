import django_filters

from shop.models import Supplier, Product


class SupplierListFilter(django_filters.FilterSet):
    type__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Supplier
        fields = ['type__name']


class SupplierProductListFilter(django_filters.FilterSet):
    tag__name = django_filters.CharFilter(lookup_expr='icontains')
    unit_price__gt = django_filters.NumberFilter(
        field_name='unit_price', lookup_expr='gt')
    unit_price__lt = django_filters.NumberFilter(
        field_name='unit_price', lookup_expr='lt')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ['tag__name', 'unit_price__gt',
                  'unit_price__lt', 'is_available']
