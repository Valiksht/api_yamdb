from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Проверко, является ли пользователь админом или суперпользователем."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
            )
        )

class IsModerator(permissions.BasePermission):
    """Проверка является ли пользователь модератором."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )
