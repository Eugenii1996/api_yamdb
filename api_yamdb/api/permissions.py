from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrModeratorOrOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or user.role == 'moderator'
            or user.is_superuser
            or obj.author == request.user
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user != AnonymousUser():
            return (
                user.role == 'admin'
                or user.is_superuser
            )
        return request.method in SAFE_METHODS
