from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsOwnerOrReadOnly(BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.username == '':
            return request.method in SAFE_METHODS
        return (
            request.method in SAFE_METHODS
            or user.role == 'admin'
            or user.is_superuser
        )
