from rest_framework.permissions import (
    BasePermission, SAFE_METHODS)


class AdminOrReadOnly(BasePermission):
    message = 'Изменение доступно только администратору!'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
        )
