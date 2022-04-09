from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .viewsets import CreateGetDeleteViewSet
from .permissions import ReadOnly, IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer, TitleSerializer, TitleListSerializer
)
from reviews.models import Category, Genre, Comment, Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateGetDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_destroy(self, instance):
        instance.delete(slug=self.kwargs.get('slug'))


class GenreViewSet(CreateGetDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_destroy(self, instance):
        instance.delete(slug=self.kwargs.get('slug'))


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer

    def perform_destroy(self, instance):
        instance.delete(id=self.kwargs.get('titles_id'))
