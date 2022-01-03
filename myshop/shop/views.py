from django.shortcuts import render
from django.urls.base import reverse
from users.models import CustomUser
from shop.forms import LoginForm, SupplierForm
from shop.models import Supplier, Product
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

# Create your views here.


class Login(View):
    """This view is for logging in"""

    form = LoginForm()

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, 'Login Succed.')
                next = request.GET.get('next')
                if next:
                    return redirect(request.GET.get('next'))
                return HttpResponseRedirect('/shop/base')

            return HttpResponseRedirect('/shop/login')

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/login.html', {'form': self.form})


class Base(View):
    """This view is for Base"""
    form = LoginForm()

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/base.html', {'form': self.form})


class DashboardView(LoginRequiredMixin, ListView):
    """This view is for showing user's shops"""
    login_url = 'login'
    model = Supplier
    template_name = 'shop/index.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.available.filter(custom_user=self.request.user)


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """This class view is for creating a post after user has been logged in """
    login_url = 'login'
    form_class = SupplierForm
    success_url = reverse_lazy('shop:dashboard')
    template_name = 'shop/supplier_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.custom_user = self.request.user
        return super(SupplierCreateView, self).form_valid(form)


class SupplierDetailView(LoginRequiredMixin, DetailView):
    """This view is for showing supplier detail to its owner"""
    model = Supplier
    login_url = 'login'

    def get_queryset(self, *args, **kwargs):
        return self.model.available.filter(custom_user=self.request.user)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     form = CommentForm()
    #     context['comment_list'] = Comment.objects.filter(post=context['post'])
    #     context['tag_list'] = Tag.objects.filter(post=context['post'])
    #     context['form'] = form
    #     if self.request.user != 'AnonymousUser':
    #         context['user'] = self.request.user
    #     return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.custom_user != self.request.user:
            raise PermissionDenied
        return super(SupplierDetailView, self).dispatch(request, *args, **kwargs)


class SupplierEditView(LoginRequiredMixin, UpdateView):
    """ This class view is for editing a Post """
    login_url = 'login'
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy('shop:dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.custom_user != self.request.user:
            raise PermissionDenied
        return super(SupplierEditView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.status = 'PEND'
        return super(SupplierEditView, self).form_valid(form)


class DeleteSupplier(LoginRequiredMixin, View):
    """This view is for delte a supplier"""
    template_name = 'shop/supplier_detail.html'
    model = Supplier
    form_class = SupplierForm

    def post(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        print(request)
        slug = kwargs['slug']
        self.model.objects.filter(slug=slug).update(status='DELE')
        return redirect(reverse('shop:dashboard'))


class SupplierView(View):
    """This class view is for creating and showing comments """

    def get(self, request, *args, **kwargs):
        view = SupplierDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DeleteSupplier.as_view()
        return view(request, *args, **kwargs)


class SupplierProductView(LoginRequiredMixin, ListView):
    """This view is for showing supplier's product"""
    login_url = 'login'
    model = Product
    # template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):
        self.supplier_slug = kwargs['slug']
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(supplier__slug=self.supplier_slug)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """This view is for showing supplier detail to its owner"""
    model = Product
    login_url = 'login'
    slug_url_kwarg = 'product_slug'

    # def get_queryset(self, *args, **kwargs):
    #     return self.model.available.filter(custom_user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        print(9999329489238492)
        obj = self.get_object()
        if obj.supplier.custom_user != self.request.user:
            raise PermissionDenied
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    # def slug_url_kwarg(self):
    #     """Get the name of a slug in url ."""
    #     return 'product_slug'
