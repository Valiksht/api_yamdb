from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment
from django.contrib.auth import get_user_model

import datetime as dt

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории (Category)."""

    class Meta:
        model = Category
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанра (Genre)."""

    class Meta:
        model = Genre
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведения (Title)."""

    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, data):
        return data

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли'
                '(год выпуска не может быть больше текущего).'
            )
        return True

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва (Review)."""

    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['pub_date', 'author']

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария (Comment)."""

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['pub_date', 'author']

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя (User)."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
