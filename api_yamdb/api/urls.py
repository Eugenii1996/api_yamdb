from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import (GetTokenAPIView, RegisterUserViewSet, UsersMeAPIView,
                    UsersViewSet)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r'categories/(?P<slug>\w+)',
                   CategoryViewSet, basename='categorie')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(r'genres/(?P<slug>\w+)',
                   GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('auth/signup', RegisterUserViewSet)
router_v1.register('users', UsersViewSet)

urlpatterns = [
    path('users/me/', UsersMeAPIView.as_view()),
    path('auth/token/', GetTokenAPIView.as_view()),
    path('', include(router_v1.urls)),

]


