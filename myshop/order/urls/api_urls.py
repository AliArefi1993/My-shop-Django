from django.urls import path
from order.views.api_views import OrderListPendView

app_name = 'order_api'
urlpatterns = [

    path('order/',
         OrderListPendView.as_view(), name='order_pend_list'),

]
