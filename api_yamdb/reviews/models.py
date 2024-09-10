from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

from api_yamdb.constants import (
    USER_ROLE,
    MODERATOR_ROLE,
    ADMIN_ROLE,
    NAME_LENGTH,
    SLUG_LENGTH,
    ROLE_LENGTH,
    USER_NAME_LENGTH,
    CODE_LENGTH,
    EMAIL_LENGTH
)
from .validators import simbol_validate, validate_year


class BaseGenreCategoryModel(models.Model):
    """Абстрактная модель для джанров и категорий."""

    name = models.CharField(max_length=NAME_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name', 'slug')

    def __str__(self):
        """Функция строкового представления."""

        return self.name


class Category(BaseGenreCategoryModel):
    """Модель категорий к произведениям."""

    class Meta(BaseGenreCategoryModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class Genre(BaseGenreCategoryModel):
    """Модель жанров к произведениям."""

    class Meta(BaseGenreCategoryModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""

    name = models.CharField(max_length=NAME_LENGTH)
    year = models.SmallIntegerField(db_index=True, validators=[validate_year])
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',

    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name', 'year')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def clean(self) -> None:
        self.validate_year(self.year)

    def __str__(self):
        """Функция строкового представления."""
        return self.name


class BaseReviewCommentModel(models.Model):
    """Абстрактная модель для отзывов и комментариев."""
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('author', 'pub_date')

    def __str__(self):
        return f'{self.__class__.__name__} от {self.author}'


class Review(BaseReviewCommentModel):
    """Модель отзыва."""
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, "Оценка не может быть меньше 1")]
    )

    class Meta(BaseReviewCommentModel.Meta):
        ordering = ('title', 'author')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        """Функция строкового представления."""
        return f'Отзыв от {self.author} на {self.title}'


class Comment(BaseReviewCommentModel):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(BaseReviewCommentModel.Meta):
        ordering = ('review', 'author')
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Функция строкового представления."""
        return f'Коммент от {self.author} на {self.review}'


class User(AbstractUser):
    """Кастомная модель пользователя."""

    ROLE_CHOICES = (
        (USER_ROLE, 'Пользователь'),
        (MODERATOR_ROLE, 'Модератор'),
        (ADMIN_ROLE, 'Админ'),
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_LENGTH,
        unique=True,
        error_messages={
            'unique': "Пользователь с такой почтой уже существует."
        },
        help_text="Введите свою почту."
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=USER_NAME_LENGTH,
        unique=True,
        validators=[simbol_validate],
        error_messages={
            'unique': "Пользователь с таким именем уже существует."
        },
        help_text="Введите уникальное имя пользователя."
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_NAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_NAME_LENGTH,
        blank=True
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(verbose_name='Роль', max_length=ROLE_LENGTH,
                            choices=ROLE_CHOICES, default=USER_ROLE)
    confirmation_code = models.CharField(max_length=CODE_LENGTH, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Функция строкового представления."""
        return f'Пользователь {self.username}'

    @property
    def is_user(self):
        return self.role == USER_ROLE

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE

    @property
    def is_admin(self):
        return (self.role == ADMIN_ROLE
                or self.is_superuser
                or self.is_staff)
