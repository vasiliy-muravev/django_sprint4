from django.urls import path

from .views import index, post_detail, category_posts, create_post, profile

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('posts/', create_post, name='create_post'),
    path('profile/<str:username>/', profile, name='profile'),
    path(
        'category/<slug:category_slug>/', category_posts, name='category_posts'
    ),
]
