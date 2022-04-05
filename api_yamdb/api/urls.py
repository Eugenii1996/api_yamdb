from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import (GetTokenAPIView, RegisterUserViewSet, UsersMeAPIView,
                         UsersViewSet)

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

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
router_v1.register(
    r'titles/(?P<title_id>\\d+)/reviews', 
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\\d+)/reviews/?P<review_id>\\d+/comments', 
    CommentViewSet, 
    basename='comments'
)

urlpatterns = [
    path('users/me/', UsersMeAPIView.as_view()),
    path('auth/token/', GetTokenAPIView.as_view()),
    path('', include(router_v1.urls)),
]
