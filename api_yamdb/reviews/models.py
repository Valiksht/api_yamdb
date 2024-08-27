from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser (AbstractUser):
    """Кастомная модель пользователя."""
    
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ'),
    )

    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES)
    confirmation_code = models.CharField(max_length=60, blank=True)


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы."""

    name = models.CharField(max_length=200)
    year = models.IntegerField()
