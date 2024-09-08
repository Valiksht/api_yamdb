from django.contrib import admin

from .models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
    User
)


class CategoryAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)


class TitleAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'name',
        'year',
        'description'
    )
    list_editable = (
        'year',
        'description'
    )
    search_fields = ('name', 'year')
    list_filter = ('category', 'genre')
    list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('title',)
    list_filter = ('score',)
    list_display_links = ('title',)


class CommentAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    search_fields = ('review',)
    list_filter = ('author',)
    list_display_links = ('review',)


class UserAdmin(admin.ModelAdmin):
    admin.site.empty_value_display = 'Не задано'
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    list_editable = (
        'role',
    )
    search_fields = ('username',)
    list_filter = ('role',)
    list_display_links = ('username',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
