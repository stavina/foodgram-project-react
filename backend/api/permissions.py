from rest_framework import permissions


class AuthorOrAdminOrReadOnly(permissions.BasePermission):
    """Доступ автора и администратора."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ администратора."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)
