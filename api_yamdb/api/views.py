from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Avg
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (AdminOrReadOnly, IsAdmin,
                          IsAdminOrModeratorOrOwnerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterUserSerializer,
                          ReviewSerializer, TitleListSerializer,
                          TitleSerializer, TokenSerializer, UsersMeSerializer,
                          UsersSerializer)
from .utils import send_confirmation_code
from .viewsets import CreateGetDeleteViewSet
from reviews.models import Category, Genre, Review, Title

codegen = PasswordResetTokenGenerator()
User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class CategoryGenreViewSet(CreateGetDeleteViewSet):
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter
    ordering = ('-year', 'name', 'category')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    """Вьюсет, для регистрации пользователя и отправки смс с кодом"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        confirmation_code = Token.generate_key()
        user = User.objects.filter(**data).first()
        if user:
            confirmation_code = user.confirmation_code
        else:
            serializer.is_valid(raise_exception=True)
            User.objects.create(**serializer.validated_data,
                                confirmation_code=confirmation_code)
        send_confirmation_code(confirmation_code,
                               email=serializer.validated_data['email'])
        return Response(data, status=status.HTTP_200_OK)


class GetTokenAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if codegen.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта /users/"""

    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UsersMeSerializer(request.user)
            return Response(serializer.data)
        serializer = UsersMeSerializer(request.user,
                                       data=request.data,
                                       partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
