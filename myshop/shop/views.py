from django.shortcuts import render
from users.models import CustomUser
from shop.forms import LoginForm, SupplierForm
from shop.models import Supplier
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
        print('logged in')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                print('logged in')
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
        return self.model.objects.filter(custom_user=self.request.user)


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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     form = CommentForm()
    #     context['comment_list'] = Comment.objects.filter(post=context['post'])
    #     context['tag_list'] = Tag.objects.filter(post=context['post'])
    #     context['form'] = form
    #     if self.request.user != 'AnonymousUser':
    #         context['user'] = self.request.user
    #     return context


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


# class SupplierDeleteView(LoginRequiredMixin, DeleteView):
#     """This class delete the selected Post from database"""
#     model = Supplier
#     success_url = reverse_lazy('dashboard')

#     def dispatch(self, request, *args, **kwargs):
#         """ Making sure that only authors can delete stories """
#         obj = self.get_object()
#         if obj.owner != self.request.user:
#             raise PermissionDenied
#         return super(PostDeleteView, self).dispatch(request, *args, **kwargs)
