from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from order.models import OrderItem, Order
from shop.models import Supplier
from django.core.exceptions import PermissionDenied
from order.filters import OrderItemFilter
from django.db.models.aggregates import Count, Max, Sum


class OrderItemEditView(LoginRequiredMixin, View):
    """This view is for edit order item status"""
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        f = OrderItemFilter(self.request.GET, queryset=self.model.objects.filter(
            product__supplier__slug=self.supplier_slug))
        context['filter'] = f
        return context


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


class ReoprtSupplierSiailsView(LoginRequiredMixin, DetailView):
    """This view is for showing to supplier's sails in a chart """
    login_url = 'login'
    model = Supplier
    template_name = 'order/supplier_sail_chart.html'

    def get_queryset(self, *arg, **kwargs):
        return Supplier.available.filter(slug=self.kwargs['slug'], custom_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chart_data = OrderItem.objects.filter(product__supplier=context['supplier'], product__supplier__status='CONF', status='PAID').values('date__date').annotate(
            total_price1=Sum('price')).order_by('date__date')
        context['chart_data'] = chart_data
        return context


class SupplierCustomerList(LoginRequiredMixin, DetailView):
    """This view is for showing to supplier's customer list"""

    template_name = 'order/supplier_customer_list.html'
    login_url = 'login'
    model = Supplier

    def get_queryset(self, *arg, **kwargs):
        return Supplier.available.filter(slug=self.kwargs['slug'], custom_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_order'] = OrderItem.objects.filter(product__supplier=context['supplier'], product__supplier__status='CONF', status='PAID'
                                                             ).values('order__customer', 'order__customer__customer_username', 'order__customer__custom_user__image').annotate(
            last_order=Max('date'),
            order_count=Count('id'),
            purchase_price=Sum('price'),
            purchase_quantity=Sum('quantity')
        ).order_by()
        return context
