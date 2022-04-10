from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        user = User.objects.filter(username=attrs['username']).first()
        if user is None:
            raise NotFound('Пользователь с указанным username не существует')
        if attrs['confirmation_code'] != user.confirmation_code:
            raise ValidationError('Код недействителен для этого username')
        return attrs


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для auth, users"""

    role = serializers.ChoiceField(choices=settings.ROLE_CHOICES,
                                   default='user')
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']


class UsersMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
