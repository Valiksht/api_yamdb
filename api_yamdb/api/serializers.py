from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

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
    rating = serializers.SerializerMethodField()

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
    
    def get_rating(self, obj):
        review = obj.reviews.all()
        if review.exists():
            sr_reting = 0
            for score in review:
                sr_reting =+ score.score
            reting = sr_reting / review.count()
            return reting
        return 0

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва (Review)."""
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # title = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CreateOnlyDefault(context.get('view').kwargs['title_id']))
    author = serializers.SerializerMethodField()
    score = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['pub_date', 'author', 'title']

    def validate(self, data):
        author = self.context.get('request').user
        title = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (Review.objects.filter(author=author, title=title).exists()
                and method == 'POST'
        ):
            raise serializers.ValidationError(
                'Вы уже сотавляли отзывк этому произведению!'
            )
        return data
    
    def validate_score(self, data):
        if 1 > data or data > 10:
            raise serializers.ValidationError(
                'Балл должен быть в диапазоне от 1 до 10'
            )
        return data

    def get_author(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария (Comment)."""
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['pub_date', 'author', 'review']

    def get_author(self, obj):
        return obj.author.username

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя (User)."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    # def update(self, instance, validated_data):

    #     validated_data.pop('role', None)
    #     return super().update(instance, validated_data)
