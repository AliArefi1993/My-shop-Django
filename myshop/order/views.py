from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from order.models import OrderItem
from django.core.exceptions import PermissionDenied


class OrderItemEditView(LoginRequiredMixin, View):
    """This view is for delte a supplier"""
    model = OrderItem

    def post(self, request, *args, **kwargs):
        self.model.objects.filter(pk=request.POST['order_id']).update(
            status=request.POST['status'])

        return redirect(reverse('order:order_item', kwargs={'slug': request.POST['slug']}))


class SupplierOrderItemView(LoginRequiredMixin, ListView):
    """This view is for showing supplier's order items"""
    login_url = 'login'
    model = OrderItem

    def get(self, request, *args, **kwargs):
        self.supplier_slug = kwargs['slug']
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        self.queryset = self.model.objects.filter(
            product__supplier__slug=self.supplier_slug)
        return super().get_queryset(*args, **kwargs)


class OrderItemDetailView(LoginRequiredMixin, DetailView):
    """This view is for showing order item's detail to its supplier's owner"""
    model = OrderItem
    login_url = 'login'
    slug_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.product.supplier.custom_user != self.request.user:
            raise PermissionDenied
        return super(OrderItemDetailView, self).dispatch(request, *args, **kwargs)
