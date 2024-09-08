from django.core.validators import RegexValidator

simbol_validate = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message=('Введите допустимое имя пользователя.'
             'Допустимые символы только буквы цифры'
             'и символы "@", ".", "+", "-", "_".'),
    code='invalid_username'
)
