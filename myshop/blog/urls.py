from django.urls import path
# from .views import post_list
from blog.views import ProfileView, CategoryPostListView, TagListView, TagPostListView, TagEditView, \
    PostsListView, PostDetailView, CategoryListView, Login, Logout, SignUpView, TagDeleteView, TagCreateView,\
    CategoryEditView, CategoryDeleteView, CategoryCreateView, DashboardView, PostCreateView, PostCommentView, SearchView, PostEditView,\
    PostDeleteView, ContactFormView
urlpatterns = [

    # path('login', user_login, name='login'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('post-list', PostsListView.as_view(), name='post_list'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('search', SearchView.as_view(), name='search'),
    path('post-create', PostCreateView.as_view(), name='post_create'),

    path('post-detail/<slug:slug>/', PostCommentView.as_view(), name='postdetail'),
    path('post-edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),


    path('category-list', CategoryListView.as_view(), name='category_list'),
    path('category-posts-list/<int:id>/',
         CategoryPostListView.as_view(), name='category_post'),

    path('tag-list', TagListView.as_view(), name='tag_list'),
    path('tag-posts-list/<int:id>/',
         TagPostListView.as_view(), name='tag_post'),
    path('tag-edit/<int:pk>', TagEditView.as_view(), name='tag_edit'),
    path('tag-delete/<int:pk>', TagDeleteView.as_view(), name='tag_delete'),
    path('tag-create/', TagCreateView.as_view(), name='tag_create'),

    path('category-edit/<int:pk>', CategoryEditView.as_view(), name='category_edit'),
    path('category-delete/<int:pk>',
         CategoryDeleteView.as_view(), name='category_delete'),
    path('category-create/', CategoryCreateView.as_view(), name='category_create'),

    path('contact/', ContactFormView.as_view(), name='contact'),


]
