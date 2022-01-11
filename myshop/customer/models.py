from django.db import models
from users.models import CustomUser


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


class ImageTest(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name
