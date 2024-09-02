from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Проверка, является ли пользователь администратором или суперпользователем."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser
            )
        )

class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'moderator'
        )

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Разрешения для анонимных пользователей (только чтение) и аутентифицированных (все действия)."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
