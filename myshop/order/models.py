from django.db import models
from django.db.models.deletion import CASCADE
from shop.models import Product
from shop.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField(blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)

    CANCELED = 'CANC'
    PENDING = 'PEND'
    PAID = 'PAID'
    STATUS = [
        (PAID, 'Paid'),
        (PENDING, 'pending'),
        (CANCELED, 'Canceled'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default=PENDING,
    )

    def __str__(self):
        return f'{self.customer.customer_username} : {self.order_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.order.customer.customer_username} : {self.product} '
