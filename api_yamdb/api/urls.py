from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r'categories/(?P<slug>\w+)',
                   CategoryViewSet, basename='categorie')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(r'genres/(?P<slug>\w+)',
                   GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
