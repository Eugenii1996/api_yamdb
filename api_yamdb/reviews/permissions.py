from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Права только у админа"""

    def has_permission(self, request, view):
        return request.user.is_admin()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj
