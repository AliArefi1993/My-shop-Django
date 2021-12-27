from django import forms
from .models import Tag, Category, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, BadHeaderError


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


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
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class SimpleModelForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=255)
    password = forms.CharField(label='password', widget=forms.PasswordInput)


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'tag', 'like']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    name = forms.CharField()
    email_address = forms.EmailField(max_length=150)

    def send_email(self):

        subject = "Website Inquiry"
        body = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email_address'],
            'message': self.cleaned_data['message'],
        }
        message = "\n".join(body.values())
        try:
            send_mail(subject, message, 'arefi_ali90@yahoo.com',
                      ['arefi_ali90@yahoo.com'])
            return True
        except BadHeaderError:
            return False
