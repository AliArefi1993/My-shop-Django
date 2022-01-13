from django.urls import path
from order.views.api_views import OrderListPendView, OrderListPreviousView, OrderPayView, OrderAddItemView

app_name = 'order_api'
urlpatterns = [
    path('order/<int:pk>/pay/',
         OrderPayView.as_view(), name='order_pay'),
    path('order/<int:pk>/additem/',
         OrderAddItemView.as_view(), name='order_add_item'),
    path('order/pend/',
         OrderListPendView.as_view(), name='order_pend_list'),
    path('order/previous/',
         OrderListPreviousView.as_view(), name='order_previous_list'),

]
