from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin, IsOwner
from .serializers import (CustomJWTSerializer, RegisterUserSerializer,
                          UsersSerializer)

User = get_user_model()


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет, для регистрации пользователя и отправки смс с кодом"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        confirmation_code = Token.generate_key()
        send_mail(
            subject='Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email='confirmationcode@mail.ru',
            recipient_list=['user@mail.ru']
        )
        User.objects.update_or_create(user,
                                      confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetTokenAPIView(APIView):
    """Выдача токена"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CustomJWTSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK)

        return Response({
            'confirmation code': 'Некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта /users/"""

    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        confirmation_code = Token.generate_key()
        send_mail(
            subject='Confirmation code',
            message=f'Your confirmation code {confirmation_code}',
            from_email='confirmationcode@mail.ru',
            recipient_list=['user@mail.ru']
        )
        User.objects.update_or_create(user,
                                      confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersMeAPIView(APIView):
    """Обработка эндпоинта users/me/"""

    permission_classes = (IsOwner,)

    def get(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username)
        serializer = UsersSerializer(user,
                                     data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
