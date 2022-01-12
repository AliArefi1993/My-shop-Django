
from django.urls import path
from shop.views.api_views import SupplierListView


app_name = 'shop_api'
urlpatterns = [

    path('supplier/',
         SupplierListView.as_view(), name='supplier'),
    # path('profile/<int:pk>',
    #      CustomerProfileUpdateDetailٰView.as_view(), name='profile'),


]
