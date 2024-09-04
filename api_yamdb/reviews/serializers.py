from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

import re

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
