from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from reviews.permissions import IsAdmin, IsOwner
from reviews.serializers import (CustomJWTSerializer, RegisterUserSerializer,
                                 UsersMeSerializer, UsersSerializer)

User = get_user_model()


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code {confirmation_code}',
        from_email='confirmationcode@mail.ru',
        recipient_list=[email]
    )


class RegisterUserAPIView(generics.CreateAPIView):
    """Вьюсет, для регистрации пользователя и отправки смс с кодом"""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            data = request.data.dict()
        else:
            data = request.data
        user = User.objects.filter(username=data['username']).first()
        serializer = self.serializer_class(data=data)
        if user:
            if user.confirmation_code:
                if 'Authorization' in request.headers:
                    serializer.is_valid(raise_exception=True)
                    return
            send_confirmation_code(user.confirmation_code, data['email'])
            return Response('Код повторно выслан вам на почту',
                            status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        confirmation_code = Token.generate_key()
        send_confirmation_code(confirmation_code, data['email'])
        User.objects.create(confirmation_code=confirmation_code,
                            **data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'


class UsersMeAPIView(APIView):
    """Обработка эндпоинта users/me/"""

    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username)
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username)
        serializer = UsersMeSerializer(user,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
