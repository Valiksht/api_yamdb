# api_yamdb
Проект YaMDB предоставляет REST API для управления произведениями, отзывами, комментариями и рейтингами. Он использует Django и Django REST Framework для реализации своей функциональности.

## Установка и настройка

### Использованные технологии

- Python 3.9 или выше
- Django 4.x
- Django REST Framework 3.x
- Django REST Framework Simple JWT
- Django Filters

### Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/api_yamdb.git
    cd api_yamdb
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/Scripts/activate  
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:

    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя для доступа к административной панели:

    ```bash
    python manage.py createsuperuser
    ```

6. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

## Использование

### Адреса API

- **Регистрация и аутентификация:**

    - `POST /api/v1/auth/signup/` - Регистрация пользователя
    - `POST /api/v1/auth/token/` - Получение JWT токена

- **Произведения:**

    - `GET /api/v1/titles/` - Список произведений
    - `POST /api/v1/titles/` - Создание произведения
    - `GET /api/v1/titles/{id}/` - Получение информации о произведении
    - `PUT /api/v1/titles/{id}/` - Обновление произведения
    - `DELETE /api/v1/titles/{id}/` - Удаление произведения

- **Категории:**

    - `GET /api/v1/categories/` - Список категорий
    - `POST /api/v1/categories/` - Создание категории
    - `GET /api/v1/categories/{id}/` - Получение информации о категории
    - `PUT /api/v1/categories/{id}/` - Обновление категории
    - `DELETE /api/v1/categories/{id}/` - Удаление категории

- **Жанры:**

    - `GET /api/v1/genres/` - Список жанров
    - `POST /api/v1/genres/` - Создание жанра
    - `GET /api/v1/genres/{id}/` - Получение информации о жанре
    - `PUT /api/v1/genres/{id}/` - Обновление жанра
    - `DELETE /api/v1/genres/{id}/` - Удаление жанра

- **Отзывы:**

    - `GET /api/v1/reviews/` - Список отзывов
    - `POST /api/v1/reviews/` - Создание отзыва
    - `GET /api/v1/reviews/{id}/` - Получение информации об отзыве
    - `PUT /api/v1/reviews/{id}/` - Обновление отзыва
    - `DELETE /api/v1/reviews/{id}/` - Удаление отзыва

- **Комментарии:**

    - `GET /api/v1/comments/` - Список комментариев
    - `POST /api/v1/comments/` - Создание комментария
    - `GET /api/v1/comments/{id}/` - Получение информации о комментарии
    - `PUT /api/v1/comments/{id}/` - Обновление комментария
    - `DELETE /api/v1/comments/{id}/` - Удаление комментария

## Тестирование

Для запуска тестов используйте команду:

### Авторы и исполнители проекта

Рубанов Валентин: https://github.com/Valiksht
Алина Гробова: https://github.com/gorbovaaa
Алексей Московцев: https://github.com/alexmos2
```bash
pytest