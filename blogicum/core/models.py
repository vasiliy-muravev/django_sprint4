from django.db import models


# Абстрактная PublishedModel модель
class PublishedModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
        help_text='Дата публикации может быть использована при сортировке'
    )

    class Meta:
        abstract = True
