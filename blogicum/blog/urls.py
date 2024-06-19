from django.urls import path

from .views import post_detail, category_posts, ProfileView, EditProfileView, PostListView, \
    CategoryListView, PostCreateView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path(
        'posts/create/',
        PostCreateView.as_view(),
        name='create_post'
    ),
    # path('posts/', create_post, name='create_post'),
    path(
        'category/<slug:category_slug>/',
        CategoryListView.as_view(),
        name='category_posts'
    ),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
]
