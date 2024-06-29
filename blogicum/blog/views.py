from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView,
    CreateView,
    DeleteView
)

from .forms import UserForm, PostForm, CommentForm
from .models import User, Post, Category, Comment
from .mixin import (
    CommentSuccessUrlMixin,
    OnlyAuthorMixin,
    PostMixin,
    PostFormMixin
)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        return Post.published_posts.all()


class PostCreateView(PostMixin, PostFormMixin, CreateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            Post.published_posts,
            pk=self.kwargs.get('post_id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        context['form'] = CommentForm()
        return context


class PostUpdateView(
    OnlyAuthorMixin,
    PostMixin,
    PostFormMixin,
    CommentSuccessUrlMixin,
    UpdateView
):
    form_class = PostForm

    def get_object(self, **kwargs):
        return get_object_or_404(
            Post,
            pk=self.kwargs['post_id']
        )


class PostDeleteView(OnlyAuthorMixin, PostMixin, DeleteView):
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs[self.pk_url_kwarg])
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = post
            form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs[self.pk_url_kwarg]}
        )


class CommentUpdateView(OnlyAuthorMixin, CommentSuccessUrlMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(OnlyAuthorMixin, CommentSuccessUrlMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

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
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        paginator = Paginator(self.get_queryset(), 10)
        page_obj = paginator.get_page(self.request.GET.get('page'))
        context['page_obj'] = page_obj
        return context


class ProfileListView(ListView):
    model = User
    template_name = 'blog/profile.html'

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        if self.request.user == self.get_object():
            return Post.objects.filter(
                author_id=self.get_object().id,
            )
        return Post.published_posts.filter(
            author_id=self.get_object().id,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        paginator = Paginator(self.get_queryset().order_by('-pub_date'), 10)
        context['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
