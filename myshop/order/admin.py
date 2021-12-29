from django.contrib import admin
from order.models import Order, OrderItem, EmailCustomer, EmailSupplier


@admin.register(EmailCustomer)
class EmailCustomerAdmin(admin.ModelAdmin):
    list_display = ('order', 'status',)
    list_filter = ('status',)
    search_fields = ('order__order_number',)


@admin.register(EmailSupplier)
class EmailCustomerAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'status',)
    list_filter = ('status',)
    search_fields = ('order_item__product__name',)


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
