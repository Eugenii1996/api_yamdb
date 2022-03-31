from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Comment, Review, Title
from .permissions import IsOwnerOrReadOnly

from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id')) 
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
#надо понять в чем отличие от класса комментариев


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        #требуется доработка
