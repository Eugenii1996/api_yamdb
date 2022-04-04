from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, APIToken

router = DefaultRouter()
router.register('signup', RegisterUserViewSet)

urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/token/', APIToken.as_view())
]
