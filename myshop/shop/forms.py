from django import forms
from shop.models import Product
from django.contrib.auth.forms import UserCreationForm
from shop.models import Supplier
from users.models import CustomUser

User = CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=255)
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'description', 'image',
                  'country', 'state', 'city', 'address', 'post_code', 'type']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'image',
                  'quantity', 'unit_price', 'is_discontinued', 'is_available', 'tag']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'phone',
            'first_name',
            'last_name',
            'email',
            'national_code',
            'password1',
            'password2',
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = [
            'phone',
            'first_name',
            'last_name',
            # 'email',
            'image'
        ]
