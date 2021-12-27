from django.shortcuts import render, redirect
from .models import Post, Comment, Category, Tag
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import View
from blog.forms import LoginForm, SignUpForm, ProfileForm, TagForm, CategoryForm, PostForm, CommentForm, ContactForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.core.exceptions import PermissionDenied


class ProfileView(LoginRequiredMixin, UpdateView):
    """" user can edit its information here."""
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('login')
    template_name = 'blog/profile.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only user can update its pprofile """
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    """" new user can sign up here."""
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'blog/signup.html'


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
                return HttpResponseRedirect('/blog/dashboard')

            return HttpResponseRedirect('/blog/login')

    def get(self, request, *args, **kwargs):
        return render(request, 'blog/login.html', {'form': self.form})


class Logout(View):
    """This view is for logging out"""

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(
            request, messages.SUCCESS, 'User Logged out.')
        return redirect('login')


class AuthorCreateView(SuccessMessageMixin, CreateView):
    """This view is for creating a post"""
    model = Post
    success_url = '/success/'
    success_message = "%(name)s was logged in successfully"


class DashboardView(LoginRequiredMixin, ListView):
    """This view is for showing user's posts"""
    login_url = 'login'
    model = Post
    template_name = 'blog/dashboard.html'

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(owner=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    """This class view is for creating a post after user has been logged in """
    login_url = 'login'
    form_class = PostForm
    success_url = reverse_lazy('dashboard')
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostsListView(ListView):
    """This view is for showing all posts to any client"""
    model = Post


class PostDetailView(DetailView):
    """This view is for showing any post to any client"""
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context['comment_list'] = Comment.objects.filter(post=context['post'])
        context['tag_list'] = Tag.objects.filter(post=context['post'])
        context['form'] = form
        if self.request.user != 'AnonymousUser':
            context['user'] = self.request.user
        return context


class PostEditView(LoginRequiredMixin, UpdateView):
    """This class view is for editing a Post"""
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied
        return super(PostEditView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """This class delete the selected Post from database"""
    model = Post
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete stories """
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)


class CommentView(LoginRequiredMixin, CreateView):
    """This class view is for creating comment """

    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        self.current_post = Post.objects.get(slug=self.kwargs['slug'])
        obj.post = self.current_post
        return super(CommentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('postdetail', kwargs={'slug': self.kwargs['slug']})


class PostCommentView(View):
    """This class view is for creating and showing comments """

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentView.as_view()
        return view(request, *args, **kwargs)


class CategoryListView(LoginRequiredMixin, ListView):
    """This class shows the list of available category"""
    login_url = 'login'
    model = Category


class CategoryPostListView(LoginRequiredMixin, ListView):
    """This class shows the list of posts for selected category"""
    login_url = 'login'
    model = Post

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(category=self.kwargs['id'])


class CategoryEditView(LoginRequiredMixin, UpdateView):
    """This class view is for editing a Category"""
    model = Category
    form_class = TagForm
    success_url = reverse_lazy('category_list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only staffs can update categories """
        obj = self.get_object()
        if not request.user.is_staff:
            raise PermissionDenied
        return super(CategoryEditView, self).dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView):
    """This class delete the selected Category from database"""
    model = Category
    success_url = reverse_lazy('category_list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only staffs can delete categories """
        obj = self.get_object()
        if not request.user.is_staff:
            raise PermissionDenied
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    """This class view is for creating a Category"""
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    template_name = 'blog/category_create.html'


class TagListView(LoginRequiredMixin, ListView):
    """This class shows the list of available tag"""
    login_url = 'login'
    model = Tag


class TagPostListView(LoginRequiredMixin, ListView):
    """This class shows the list of posts for selected tag"""
    login_url = 'login'
    model = Post

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(tag=self.kwargs['id'])


class TagEditView(UpdateView):
    """This class edit the selected tag from database"""

    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('tag_list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only staffs can update tags """
        obj = self.get_object()
        if not request.user.is_staff:
            raise PermissionDenied
        return super(TagEditView, self).dispatch(request, *args, **kwargs)


class TagDeleteView(DeleteView):
    """This class delete the selected tag from database"""
    model = Tag
    success_url = reverse_lazy('tag_list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only staffs can delete tags """
        obj = self.get_object()
        if not request.user.is_staff:
            raise PermissionDenied
        return super(TagDeleteView, self).dispatch(request, *args, **kwargs)


class TagCreateView(CreateView):
    """This class view is for creating a Tag"""
    form_class = TagForm
    success_url = reverse_lazy('tag_list')
    template_name = 'blog/tag_create.html'


class SearchView(ListView):
    """This class view is for searching in posts' title and description"""

    model = Post

    def get_queryset(self, *args, **kwargs):
        search_query = self.request.GET.get('search_box', None)
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(
            description__icontains=search_query))
        return posts


class ContactFormView(FormView):
    """This class view is for recieving user email"""

    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('dashboard')
    template_name = 'blog/contact.html'

    def form_valid(self, form):
        send_email_status = form.send_email()
        if send_email_status:
            messages.success(self.request, 'Thank you for your feedback.')

        else:

            messages.error(self.request, 'Please try again')
        return super().form_valid(form)
