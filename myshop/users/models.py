from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=13, unique=True,
                             validators=[RegexValidator(regex='09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}')])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone
