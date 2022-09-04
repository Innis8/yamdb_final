from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Класс разрешений для администраторов."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'))


class IsAdminOrListOnly(permissions.BasePermission):
    """
    Класс разрешений позволяет POST и DELETE методы только для администраторов,
    для всех остальных - только чтение (list).
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return request.method in ('DELETE',)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений позволяет POST и DELETE методы только для администраторов
    для всех остальных - только чтение.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == 'admin')


class AuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений позволяет POST для всех,
    остальные - только для авторов, модераторов, администраторов.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
                and request.user.is_authenticated)
