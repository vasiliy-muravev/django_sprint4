from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (DetailView, UpdateView,
                                  ListView, CreateView, DeleteView)
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin

from datetime import datetime

from .forms import UserForm, PostForm, CommentForm
from .models import User, Post, Category, Comment


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, **kwargs):
        post = Post.objects_all.get(pk=self.kwargs['post_id'])
        if post.author == self.request.user:
            return post
        else:
            return get_object_or_404(Post.objects.filter(
                is_published=True,
                pub_date__date__lte=datetime.now()
            ), pk=self.kwargs.get('post_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        context['form'] = CommentForm()

        return context


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, **kwargs):
        # При попытке создания комментария
        # к несуществующему посту возвращается статус 404.
        post = Post.objects_all.get(pk=self.kwargs['post_id'])
        if not post.is_published:
            raise Http404()
        return post

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return context


class CategoryListView(ListView):
    model = Category
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_object(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
        )
        if not category.is_published:
            raise Http404()
        return category

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
        paginator = Paginator(self.get_queryset().order_by('-pub_date'), 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        return context


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        if self.request.user == self.get_object():
            return Post.objects_all.filter(
                author_id=self.get_object().id,
            )
        else:
            return Post.objects.filter(
                author_id=self.get_object().id,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        paginator = Paginator(self.get_queryset().order_by('-pub_date'), 10)
        context['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, **kwargs):
        # Запрещаем заходить не владельцу
        # на страницу редактирования чужого пользователя.
        if not self.request.user.username == self.kwargs['username']:
            raise Http404()
        # Запрещаем если объект текущего пользователя
        # не совпадает с объектом из базы.
        user = User.objects.get(username=self.kwargs['username'])
        if not user == self.request.user:
            raise Http404()
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
