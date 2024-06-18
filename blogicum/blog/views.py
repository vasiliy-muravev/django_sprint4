from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView
from django.core.paginator import Paginator

from datetime import datetime

from .forms import UserForm
from .models import Post, Category, User


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = 'created_at'
    paginate_by = 10


def category_posts(request, category_slug):
    """
    Работает, но не проходит тесты.
    category = Category.objects.get(is_published=True, slug=category_slug)
    """
    category = (
        Category.objects.filter(is_published=True, slug=category_slug).first()
    )

    if not category:
        context = {'message': 'Категория не найдена'}
        return render(
            request, 'blog/not_found_error.html', context, status=404
        )

    template = 'blog/category.html'
    post_list = (
        Post.objects
        .filter(category_id=category)
        .order_by('-created_at')
    )
    context = {
        'category': category_slug,
        'post_list': post_list
    }

    return render(request, template, context)


def post_detail(request, id):
    post = Post.objects.filter(pk=id).first()

    if not post:
        context = {'message': 'Публикация не найдена'}
        return render(
            request, 'blog/not_found_error.html', context, status=404
        )

    context = {
        'post': post
    }

    return render(request, 'blog/detail.html', context)


def create_post():
    pass


class CategoryListView(ListView):
    model = Category
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])

    def get_queryset(self):
        page_obj = Post.objects.filter(
            category=self.get_object(),
            is_published=True,
            pub_date__lte=datetime.now()
        )
        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        paginator = Paginator(self.get_queryset(), 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        return context


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        return Post.objects.select_related('author').filter(
            author_id=self.get_object().id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        paginator = Paginator(self.get_queryset(), 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_object(self, **kwargs):
        return self.request.user
