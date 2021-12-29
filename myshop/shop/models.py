from django.db import models
from users.models import CustomUser
# Create your models here.


class Customer(models.Model):
    customer_username = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    post_code = models.CharField(max_length=10)
    custom_user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='customer_user')

    def __str__(self):
        return self.customer_username


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    post_code = models.CharField(max_length=10)
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    DELETED = 'DELE'
    PENDING = 'PEND'
    CONFIRMED = 'CONF'
    STATUS = [
        (CONFIRMED, 'Confirmed'),
        (PENDING, 'pending'),
        (DELETED, 'deleted'),
    ]
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default=PENDING,
    )

    def __str__(self):
        return self.supplier_name


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    unit_price = models.DecimalField(decimal_places=2, max_digits=11)
    is_discontinued = models.BooleanField()
    is_available = models.BooleanField()
    tag = models.ForeignKey(
        'Tag', on_delete=models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
