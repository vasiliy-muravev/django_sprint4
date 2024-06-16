from django.contrib import admin

from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'description',
        'slug'
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'slug',)
    list_filter = ('title', 'slug',)
    list_display_links = ('id', 'title',)
    empty_value_display = 'Не задано'


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('id', 'name',)
    empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
        'author',
        'location',
        'category',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('author', 'location', 'category')
    list_display_links = ('id', 'title',)
    empty_value_display = 'Не задано'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
