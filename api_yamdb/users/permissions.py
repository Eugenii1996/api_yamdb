from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Права только у админа"""

    def has_permission(self, request, view):
        user = request.user
        return user.role == 'admin' or user.is_superuser


class IsOwner(BasePermission):
    """Права только у владельца учетной записи"""

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username
