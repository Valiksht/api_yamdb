import datetime as dt
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

simbol_validate = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message=('Введите допустимое имя пользователя.'
             'Допустимые символы только буквы цифры'
             'и символы "@", ".", "+", "-", "_".'),
    code='invalid_username'
)


def validate_year(value):
    """Валидатор для проверки года выпуска."""

    year = dt.date.today().year
    if value > year:
        raise ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли. '
            '(год выпуска не может быть больше текущего).'
        )
