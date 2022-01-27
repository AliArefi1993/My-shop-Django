from django.db.models.query_utils import Q
from django.shortcuts import render
from django.urls.base import reverse
from users.models import CustomUser
from shop.forms import LoginForm, SupplierForm, ProductForm, SignUpForm, ProfileForm, OtpForm
from shop.models import Supplier, Product
from order.models import OrderItem
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from utils.otp_auth import VerifyTOTP
from users.tasks import send_sms
from utils.generate_key import generateKey


class SignUpView(CreateView):
    """" new user can sign up here."""
    form_class = SignUpForm
    success_url = reverse_lazy('shop:login')
    template_name = 'shop/register.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """" user can edit its information here."""
    login_url = 'shop:login'
    model = CustomUser
    form_class = ProfileForm
    success_url = reverse_lazy('shop:dashboard')
    template_name = 'shop/profile.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only user can update its profile """
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


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
                return HttpResponseRedirect('/shop/dashboard')

            return HttpResponseRedirect('/shop/login')

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/login.html', {'form': self.form})


class LogoutView(View):
    """This view is for logging out"""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(
            request, messages.SUCCESS, 'User Logged out.')
        return redirect('shop:login')


class DashboardView(LoginRequiredMixin, ListView):
    """This view is for showing user's suppliers"""
    login_url = 'shop:login'
    model = Supplier
    template_name = 'shop/index.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.available.filter(custom_user=self.request.user)


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """This class view is for creating a supplier after user has been logged in """
    login_url = 'shop:login'
    form_class = SupplierForm
    success_url = reverse_lazy('shop:dashboard')
    template_name = 'shop/supplier_create.html'
    model = Supplier

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.custom_user = self.request.user
        return super(SupplierCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.model.not_available.filter(custom_user=self.request.user):
            messages.add_message(
                request, messages.WARNING, "You can't create new supplier, beacause you have at least one supplier with the pending status.")
            return HttpResponseRedirect('/shop/dashboard')
        return super().get(request, *args, **kwargs)


class SupplierDetailView(LoginRequiredMixin, DetailView):
    """This view is for showing supplier detail to its owner"""
    login_url = 'shop:login'
    model = Supplier
    login_url = 'login'

    def get_queryset(self, *args, **kwargs):
        return self.model.available.filter(custom_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_item_list'] = OrderItem.objects.filter(
            product__supplier=context['supplier']).order_by('-order__order_date')
        return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.custom_user != self.request.user:
            raise PermissionDenied
        return super(SupplierDetailView, self).dispatch(request, *args, **kwargs)


class SupplierEditView(LoginRequiredMixin, UpdateView):
    """ This class view is for editing a supplier details """
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
    login_url = 'shop:login'
    template_name = 'shop/supplier_detail.html'
    model = Supplier
    form_class = SupplierForm

    def post(self, request, *args, **kwargs):
        slug = kwargs['slug']
        self.model.objects.filter(slug=slug).update(status='DELE')
        return redirect(reverse('shop:dashboard'))


class SupplierView(LoginRequiredMixin, View):
    """This class view is for supplier """
    login_url = 'shop:login'

    def get(self, request, *args, **kwargs):
        view = SupplierDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DeleteSupplier.as_view()
        return view(request, *args, **kwargs)


class SupplierProductView(LoginRequiredMixin, ListView):
    """This view is for showing supplier's product"""
    login_url = 'shop:login'
    model = Product

    def get(self, request, *args, **kwargs):
        self.supplier_slug = kwargs['slug']
        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        self.queryset = self.model.objects.filter(
            supplier__slug=self.supplier_slug)
        return super().get_queryset(*args, **kwargs)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """This view is for showing supplier detail to its owner"""
    model = Product
    login_url = 'shop:login'
    slug_url_kwarg = 'product_slug'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.supplier.custom_user != self.request.user:
            raise PermissionDenied
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """This class view is for creating a Product in a specified Supplier """
    login_url = 'shop:login'
    form_class = ProductForm
    template_name = 'shop/product_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.supplier = Supplier.objects.get(slug=self.kwargs['slug'])
        return super(ProductCreateView, self).form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy(
            'shop:supplier_products', kwargs=self.kwargs)
        return super().get_success_url()


class ProductEditView(LoginRequiredMixin, UpdateView):
    """ This class view is for editing a Product """
    login_url = 'shop:login'
    model = Product
    form_class = ProductForm
    slug_url_kwarg = 'product_slug'

    def get_success_url(self):
        self.success_url = reverse_lazy(
            'shop:product_detail', kwargs=self.kwargs)
        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only it's  own user can update this product """
        obj = self.get_object()
        if obj.supplier.custom_user != self.request.user:
            raise PermissionDenied
        return super(ProductEditView, self).dispatch(request, *args, **kwargs)


class SearchView(LoginRequiredMixin, ListView):
    """This class view is for searching in suppliers' name and description"""
    login_url = 'shop:login'
    model = Supplier
    template_name = 'shop/index.html'

    def get_queryset(self, *args, **kwargs):
        search_query = self.request.GET.get('search_box', None)
        suppliers = Supplier.available.filter(Q(supplier_name__icontains=search_query) | Q(
            description__icontains=search_query)).filter(custom_user=self.request.user)
        return suppliers


class OTPView(View):
    """This view is for sending otp"""

    def get(self, request, *args, **kwargs):
        phone = self.request.user.phone
        if self.request.user.phone_is_submitted == False:
            OTP = VerifyTOTP(generateKey.get_key(phone, 'verify'))
            otp = OTP.now()
            send_sms.delay(phone, otp)
            messages.add_message(
                request, messages.SUCCESS, 'OTP has been sent successfully.')
        else:
            messages.add_message(
                request, messages.WARNING, 'Your phone has already been submitted!')

        return redirect('shop:submit_phone', self.request.user.pk)


class PhoneSubmitView(LoginRequiredMixin, UpdateView):
    """ This class view is for submitting phone number """
    login_url = 'login'
    model = CustomUser
    form_class = OtpForm
    template_name = 'shop/submit_phone.html'
    success_url = reverse_lazy('shop:dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied
        return super(PhoneSubmitView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        obj = form.save(commit=False)
        phone = obj.phone
        print(self.request.POST['OTP'])
        OTP = VerifyTOTP(generateKey.get_key(phone, 'verify'))

        if OTP.verify(self.request.POST['OTP']):
            obj.phone_is_submitted = True

            """If the form is valid, save the associated model."""
            self.object = form.save()

            """If the form is valid, redirect to the supplied URL."""
            messages.add_message(
                self.request, messages.SUCCESS, 'Your phone authorised successfuly.')
            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            self.request, messages.WARNING, 'Your code is wrong!')
        return redirect('shop:submit_phone', self.request.user.pk)

        # return super(PhoneSubmitView, self).form_valid(form)
