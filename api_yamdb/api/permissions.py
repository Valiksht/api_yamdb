from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверка, является ли пользователь автором."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_authenticated
        # elif 1==1:
        elif request.method in ('PATCH', 'DELETE'):
            return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    """Проверка, является ли метод безопасным."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsAdmin(permissions.BasePermission):
    """Является ли пользователь администратором или суперпользователем."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser
        else:
            return False


class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ('POST', 'PATCH', 'DELETE'):
            return (
                request.user.is_authenticated
                and request.user.role == 'moderator'
            )

        return super().has_object_permission(request, view, obj)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Для анонимов чтение и аутентифицированных все действия."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
