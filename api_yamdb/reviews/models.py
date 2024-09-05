from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Category(models.Model):
    """Модель категорий к произведениям."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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
        'User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Коммент от {self.author} на {self.review}'


class User(AbstractUser):
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
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "Пользователь с такой почтой уже существует."
        },
        help_text="Введите свою почту."
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=150,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким именем уже существует."
        },
        help_text="Введите уникальное имя пользователя."
    )
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(verbose_name='Роль', max_length=20,
                            choices=ROLE_CHOICES, default='user')
    confirmation_code = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    @property
    def is_user(self):
        return self.role == 'user'
    
    @property
    def is_moderator(self):
        return self.role == 'moderator'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
