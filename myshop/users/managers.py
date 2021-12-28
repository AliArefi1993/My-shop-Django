from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phone:
            raise ValueError(('The Email must be set'))
        # email = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)

    # @classmethod
    # def normalize_phone(cls, phone):
    #     """
    #     Normalize the email address by lowercasing the domain part of it.
    #     """
    #     phone = phone or ''
    #     try:
    #         if phone[0] == '0':
    #             phone = '+98' + phone[1:]
    #             # +98 913 148 0548
    #     except ValueError:
    #         pass
    #     else:
    #         phone = email_name + '@' + domain_part.lower()
    #     return email
