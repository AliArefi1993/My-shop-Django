from django.contrib import admin

# Register your models here.


from users.models import CustomUser

# # Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
