from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, GetTokenAPIView, UsersViewSet

router = DefaultRouter()
router.register('signup', RegisterUserViewSet)
router.register('users', UsersViewSet)

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/token/', GetTokenAPIView.as_view())
]
