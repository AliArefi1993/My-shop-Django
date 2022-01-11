from django.urls import path
from order.views import OrderItemEditView, SupplierOrderItemView, OrderItemDetailView, ReoprtSupplierSiailsView
app_name = 'order'
urlpatterns = [

    path('order_item_edit/<int:pk>/',
         OrderItemEditView.as_view(), name='update_order_status'),

    path('supplier/<slug:slug>/order_item/',
         SupplierOrderItemView.as_view(), name='order_item'),

    path('supplier/<slug:slug>/order_item/<int:pk>',
         OrderItemDetailView.as_view(), name='order_item_detail'),

    path('supplier/<slug:slug>/sail_chart/',
         ReoprtSupplierSiailsView.as_view(), name='supplier_sail_chart'),



]
