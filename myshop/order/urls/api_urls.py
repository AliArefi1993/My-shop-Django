from django.urls import path
from order.views.api_views import OrderListPendView, OrderListPreviousView, OrderPayView

app_name = 'order_api'
urlpatterns = [
    path('order/<int:pk>/pay/',
         OrderPayView.as_view(), name='order_pay'),
    path('order/pend/',
         OrderListPendView.as_view(), name='order_pend_list'),
    path('order/previous/',
         OrderListPreviousView.as_view(), name='order_previous_list'),

]
