
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Category(models.Model):
    """Модель категорий к произведениям."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',

    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        'MyUser',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='Можно оставить только один отзыв',
            ),
        )


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коммент от {self.author} на {self.review}'


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ'),
    )
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Введите допустимое имя пользователя.',
        code='invalid_username'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с такой почтой уже существует."
        },
        help_text="Введите свою почту."
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким именем уже существует."
        },
        help_text="Введите уникальное имя пользователя."
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=20,
                            choices=ROLE_CHOICES, default='user')
    confirmation_code = models.CharField(max_length=60, blank=True)
