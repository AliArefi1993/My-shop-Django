from django.contrib import admin
from shop.models import Customer, Supplier, Tag, Type, Product
from django.utils.html import format_html


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'supplier',
                    'unit_price', 'is_discontinued', 'is_available', 'tag', 'show_image')
    list_filter = ('is_discontinued', 'is_available', 'tag')
    search_fields = ('name', 'description')

    @ admin.display(empty_value='-', description="image")
    def show_image(self, obj):
        if (obj.image):
            print(obj.image.url)

            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,

            )
        return '-'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('custom_user', 'customer_username',
                    'country', 'state', 'city', 'address', 'post_code')
    list_filter = ("country", 'state', 'city',)
    search_fields = ('custom_user', 'customer_username',)


@admin.action(description='Mark selected suppliers as confimed')
def make_confirmed(ModelAdmin, request, queryset):
    queryset.update(status='CONF')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('custom_user', 'supplier_name', 'type', 'status',
                    'country', 'state', 'city', 'address', 'post_code', 'created_date', 'image',)
    list_filter = ("country", 'state', 'city', 'type')
    search_fields = ('custom_user', 'customer_username',)
    list_editable = ('status',)
    actions = [make_confirmed]
