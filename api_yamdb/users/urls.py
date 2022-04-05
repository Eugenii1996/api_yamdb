from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GetTokenAPIView, RegisterUserViewSet, UsersMeAPIView,
                    UsersViewSet)

router = DefaultRouter()
router.register('signup', RegisterUserViewSet)
router.register('users', UsersViewSet)

urlpatterns = [
    path('users/me/', UsersMeAPIView.as_view()),
    path('', include(router.urls)),
    path('token/', GetTokenAPIView.as_view()),
]
