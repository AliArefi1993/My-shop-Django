from django.contrib import admin
from users.models import CustomUser
from customer.models import ImageTest
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('show_image', "last_name", "first_name", "phone")
    list_filter = ("date_joined", )
    search_fields = ('last_name', 'first_name', 'phone')
    fieldsets = (
        (None, {
            'fields': ("last_name", "first_name", "phone",
                       'password', 'email', 'national_code', 'image')
        }),
        ('Advanced options', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_staff', 'is_active', 'date_joined'),
        }),
    )

    @ admin.display(empty_value='-', description="image")
    def show_image(self, obj):
        if (obj.image):
            print(obj.image.url)

            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,

            )
        return '-'


@admin.register(ImageTest)
class ImageTestAdmin(admin.ModelAdmin):
    pass
