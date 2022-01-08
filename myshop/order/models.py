from django.db import models
from django.db.models.deletion import CASCADE
from shop.models import Product
from customer.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    order_date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)

    CANCELED = 'CANC'
    PENDING = 'PEND'
    PAID = 'PAID'
    STATUS = [
        (PAID, 'Paid'),
        (PENDING, 'pending'),
        (CANCELED, 'canceled'),
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
    price = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    CANCELED = 'CANC'
    PENDING = 'PEND'
    APPROVED = 'APPR'
    PAID = 'PAID'
    STATUS = [
        (PAID, 'Paid'),
        (PENDING, 'pending'),
        (APPROVED, 'approved'),
        (CANCELED, 'canceled'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default=PENDING, null=True, blank=True

    )

    def __str__(self):
        return f'{self.order.customer.customer_username} : {self.product} '


class EmailCustomer(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE)
    FAILED = 'FAIL'
    INPROGRESS = 'PROG'
    SUCCESS = 'SUCC'
    STATUS = [
        (SUCCESS, 'Succesful'),
        (INPROGRESS, 'InProgress'),
        (FAILED, 'Failed'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default=INPROGRESS,
    )


class EmailSupplier(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=CASCADE)
    FAILED = 'FAIL'
    INPROGRESS = 'PROG'
    SUCCESS = 'SUCC'
    STATUS = [
        (SUCCESS, 'Succesful'),
        (INPROGRESS, 'InProgress'),
        (FAILED, 'Failed'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default=INPROGRESS,
    )
