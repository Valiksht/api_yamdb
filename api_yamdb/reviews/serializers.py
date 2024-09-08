from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import re

from api_yamdb.constants import (
    EMAIL_LENGTH,
    USER_NAME_LENGTH
)

User = get_user_model()
ERROR_NAME = ['me']


class UserRegistrateSeriolizer(serializers.ModelSerializer):
    """Сериализатор обрабатывающий регистрацию и отправку проверочного кода."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )

    def validate_username(self, value):
        if value is None:
            raise serializers.ValidationError(
                'Поле не может быть пустым'
            )
        elif not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('Недопустимые символы!')
        elif len(value) >= USER_NAME_LENGTH:
            raise serializers.ValidationError(
                f'Превышена максимальная длина в {USER_NAME_LENGTH} символа!'
            )
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Данный username уже занят!')
        return value

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError(
                'Поле не может быть пустым'
            )
        elif len(value) >= EMAIL_LENGTH:
            raise serializers.ValidationError(
                f'Превышена максимальная длина в {EMAIL_LENGTH} символа!'
            )
        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Данный email уже занят!')
        return value

    def validate(self, attrs):
        username = attrs.get('username')
        if username in ERROR_NAME:
            raise serializers.ValidationError(
                f'Username "{username}" запрещен!'
            )
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор обрабатывающий отправку токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username', 'confirmation_code'
        )

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        if username == 'me':
            raise serializers.ValidationError(
                f'Username "{username}" запрещен!'
            )
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                'Неверная связка юзернейм и проверочный код.'
            )
        return user
