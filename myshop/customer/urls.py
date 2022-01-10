from django.urls import path
from customer.views import CreateUserView
app_name = 'customer'
urlpatterns = [

    path('register/',
         CreateUserView.as_view(), name='update_order_status'),


]
