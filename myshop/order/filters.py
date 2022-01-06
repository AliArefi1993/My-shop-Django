
import django_filters
from django import forms

from order.models import OrderItem


class OrderItemFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=forms.SelectDateWidget(years=range(2020, 2020 + 10)),
                                           field_name='order__order_date', lookup_expr='gt')
    end_date = django_filters.DateFilter(widget=forms.SelectDateWidget(years=range(2020, 2020 + 10)),
                                         field_name='order__order_date', lookup_expr='lt')

    class Meta:
        model = OrderItem
        fields = ['status', 'start_date', 'end_date']
