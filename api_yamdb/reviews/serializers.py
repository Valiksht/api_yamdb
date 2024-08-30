from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrateSeriolizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


class TokenSerializer(serializers.ModelSerializer):
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
        try:
            user = User.objects.get(
                username=username, confirmation_code=confirmation_code)
            return user
            # return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError(
                'Неверная связка юзернейм и проверочный код.'
            )
