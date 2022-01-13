from django.urls import path
from order.views.api_views import OrderListPendView, OrderListPreviousView

app_name = 'order_api'
urlpatterns = [

    path('order/pend/',
         OrderListPendView.as_view(), name='order_pend_list'),
    path('order/previous/',
         OrderListPreviousView.as_view(), name='order_previous_list'),

]
