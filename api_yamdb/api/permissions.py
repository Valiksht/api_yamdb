from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Является ли пользователь администратором или суперпользователем."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class AdminOrReadOnly(permissions.BasePermission):
    """Является ли пользователь администратором или суперпользователем."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_admin)


class AdminModeratorOrReadOnly(permissions.BasePermission):
    """Является ли пользователь администратором или суперпользователем."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ('PATCH', 'DELETE'):
            return (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
            )
