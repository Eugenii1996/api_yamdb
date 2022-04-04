from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Использование me в качестве '
                                  'username запрещено')
        return value

    class Meta:
        model = User
        fields = ['email', 'username']


class CustomJWTSerializer(TokenObtainPairSerializer):
    """Сериализатор для JWT токена"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(confirmation_code=attrs['confirmation_code']).first()
        if user is None or attrs['username'] != user.username:
            raise ValidationError('Пользователь с указанными данными не найден')
        return attrs
