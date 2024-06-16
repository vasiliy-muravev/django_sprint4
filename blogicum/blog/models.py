from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from core.models import PublishedModel

User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Название категории, не более 256 символов, '
                  'обязательное поле'
    )
    description = models.TextField(
        'Описание',
        help_text='Описание категории, обязательное поле'
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=64,
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        'Название места',
        max_length=256,
        help_text='Название места, не более 256 символов, '
                  'обязательное поле'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class BasePostManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('category', 'author', 'location')
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=now()
            )
        )


class Post(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
        help_text='Заголовок публикации, не более 256 символов, '
                  'обязательное поле'
    )
    text = models.TextField(
        'Текст',
        help_text='Текст публикации, обязательное поле'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно '
                  'делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория',
        blank=False,
        null=True
    )

    # Базовый запрос постов
    objects = BasePostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
