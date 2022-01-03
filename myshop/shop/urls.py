from django.urls import path
from shop.views import Login, Base, DashboardView, SupplierDetailView, SupplierEditView,\
    SupplierCreateView
app_name = 'shop'
urlpatterns = [

    path('login', Login.as_view(), name='login'),
    path('base', Base.as_view(), name='base'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('supplier/<slug:slug>/', SupplierDetailView.as_view(), name='detail'),
    path('supplier_create/', SupplierCreateView.as_view(), name='supplier_creat'),
    path('supplier_edit/<slug:slug>/',
         SupplierEditView.as_view(), name='supplier_edit'),

]
