from django.urls import path
from shop.views.views import Login, DashboardView, SupplierDetailView, SupplierEditView,\
    SupplierCreateView, DeleteSupplier, SupplierView, SupplierProductView, ProductDetailView,\
    ProductCreateView, ProductEditView, SignUpView, ProfileView, LogoutView, SearchView
app_name = 'shop'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('login/', Login.as_view(), name='login'),
    path('sighnup/', SignUpView.as_view(), name='sighnup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('supplier/<slug:slug>/', SupplierView.as_view(), name='detail'),
    path('supplier/<slug:slug>/products/',
         SupplierProductView.as_view(), name='supplier_products'),
    path('supplier_create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier_edit/<slug:slug>/',
         SupplierEditView.as_view(), name='supplier_edit'),
    path('supplier_delete/<slug:slug>/',
         DeleteSupplier.as_view(), name='supplier_delete'),

    path('supplier/<slug:slug>/products/<slug:product_slug>',
         ProductDetailView.as_view(), name='product_detail'),
    path('supplier/<slug:slug>/product_edit/<slug:product_slug>',
         ProductEditView.as_view(), name='product_edit'),
    path('supplier/<slug:slug>/product_create/',
         ProductCreateView.as_view(), name='product_create'),
    path('search', SearchView.as_view(), name='search'),

]
