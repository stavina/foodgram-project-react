from rest_framework import permissions


class GuestAuthenticatedReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_team


class AuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        return (
            request.method in permissions.SAFE_METHODS
            or object.author == request.user
        )
