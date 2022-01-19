from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=13, unique=True)  # ,
    #  validators=[RegexValidator(regex='09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}')])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(
        ('email address'), unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    counter = models.IntegerField(default=0)
    phone_is_submitted = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.phone
