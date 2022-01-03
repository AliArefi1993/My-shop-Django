from django import forms

from shop.models import Supplier


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=255)
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ['supplier_name', 'description', 'image',
                  'country', 'state', 'city', 'address', 'post_code', 'type']
