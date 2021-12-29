from django.contrib import admin
from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_number', 'order_date', 'status',)
    list_filter = ('status', 'order_date')
    search_fields = ('customer__customer_username', 'order_number')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity',)
    list_filter = ('quantity',)
    search_fields = ('product__name',)
