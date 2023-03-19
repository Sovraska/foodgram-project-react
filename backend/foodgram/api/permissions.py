from rest_framework import permissions


class IsAuthenticatedOrReadOnlyPermission(permissions.BasePermission):
    message = 'Проверяет авторизован ли пользователь если нет проверяет безопасный ли метод'

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in permissions.SAFE_METHODS
