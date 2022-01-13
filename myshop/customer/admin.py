from django.contrib import admin
from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('custom_user', 'customer_username',
                    'country', 'state', 'city', 'address', 'post_code')
    list_filter = ("country", 'state', 'city',)
    search_fields = ('custom_user', 'customer_username',)
