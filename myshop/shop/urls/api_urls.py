
from django.urls import path
from shop.views.api_views import SupplierListView, SupplierTypeListView, SupplierProductListView


app_name = 'shop_api'
urlpatterns = [

    path('supplier/',
         SupplierListView.as_view(), name='supplier'),
    path('supplier/type/',
         SupplierTypeListView.as_view(), name='supplier_types'),
    path('supplier/<slug:slug>/product/',
         SupplierProductListView.as_view(), name='supplier_products'),
    # path('profile/<int:pk>',
    #      CustomerProfileUpdateDetailٰView.as_view(), name='profile'),


]
