import re

from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()

ERROR_NAME = ['me']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории (Category)."""

    class Meta:
        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанра (Genre)."""

    class Meta:
        model = Genre
        fields = ['name', 'slug']


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор предоставляющий информацию о тайтлах."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        ]
        read_only_fields = fields


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
        fields = [
            'id', 'name', 'year', 'description', 'genre', 'category'
        ]
        read_only_fields = ['rating']

    def validate_year(self, value):
        title = Title()
        title.validate_year(value)
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Нельзя добавлять название больше 256 символов'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва (Review)."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False,
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['pub_date', 'author', 'title']

    def validate(self, data):
        author = self.context.get('request').user
        title = self.context.get('view').kwargs['title_id']
        method = self.context.get('request').method
        if (method == 'POST'
                and Review.objects.filter(
                    author=author,
                    title=title
                ).exists()):
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


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментария (Comment)."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        required=False,
    )

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
        read_only_fields = ['pub_date', 'author', 'review']

    # def get_author(self, obj):
    #     return obj.author.username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя (User)."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if value is None:
            raise serializers.ValidationError(
                'Поле не может быть пустым'
            )
        elif not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('Недопустимые символы!')
        elif len(value) >= 150:
            raise serializers.ValidationError('Превышена максимальная длина!')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Данный username уже занят!')
        return value

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError(
                'Поле не может быть пустым'
            )
        elif len(value) >= 254:
            raise serializers.ValidationError('Превышена максимальная длина!')
        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Данный email уже занят!')
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        user_email = User.objects.filter(email=email).first()
        user_username = User.objects.filter(username=username).first()
        if username in ERROR_NAME:
            raise serializers.ValidationError(
                f'Username "{username}" запрещен!'
            )
        elif user_email == user_username:
            return attrs
        else:
            raise serializers.ValidationError(
                f'Данный email: "{email}" или username "{username}" '
                f'занят другим пользователем!'
            )
