from django.urls import path
from order.views.api_views import OrderListPendView, OrderListPreviousView, OrderPayView, OrderAddItemView,\
    OrderSubstractItemView, OrderCreateView

app_name = 'order_api'
urlpatterns = [
    path('order/<int:pk>/pay/',
         OrderPayView.as_view(), name='order_pay'),
    path('order/',
         OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/additem/',
         OrderAddItemView.as_view(), name='order_add_item'),
    path('order/<int:pk>/subtractitem/',
         OrderSubstractItemView.as_view(), name='order_subtract_item'),
    path('order/pend/',
         OrderListPendView.as_view(), name='order_pend_list'),
    path('order/previous/',
         OrderListPreviousView.as_view(), name='order_previous_list'),

]
