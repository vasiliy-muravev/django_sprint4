from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self, **kwargs):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(
            reverse_lazy(
                'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
            )
        )


class PostMixin(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'


class PostFormMixin:
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentSuccessUrlMixin(LoginRequiredMixin):
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
