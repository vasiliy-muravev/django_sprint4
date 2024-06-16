from django.shortcuts import render

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.order_by('-created_at')[:5]
    context = {
        'post_list': post_list,
    }

    return render(request, template, context)


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
