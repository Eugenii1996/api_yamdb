import re

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.authtoken.models import Token

User = get_user_model()


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code {confirmation_code}',
        from_email='confirmationcode@mail.ru',
        recipient_list=[email]
    )


class RegisterUserSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя"""

    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Использование me в качестве '
                                  'username запрещено')
        reg = re.compile(r'^[\w.@+-]+\Z')
        if re.match(reg, value) is None:
            raise ValidationError('Только буквы, цифры и @/./+/-/_.')
        if User.objects.filter(username=value).first():
            raise ValidationError('Этот username уже занят')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError('Этот email уже занят')
        return value

    def save(self):
        email = self.validated_data['email']
        confirmation_code = Token.generate_key()
        User.objects.create(**self.validated_data,
                            confirmation_code=confirmation_code)
        send_confirmation_code(confirmation_code, email)

    class Meta:
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).first()
        if user is None:
            raise NotFound('Пользователь с указанным username не существует')
        if attrs['confirmation_code'] != user.confirmation_code:
            raise ValidationError('Код недействителен для этого username')
        return attrs


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для auth, users"""

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Использование me в качестве '
                                  'username запрещено')
        reg = re.compile(r'^[\w.@+-]+\Z')
        if re.match(reg, value) is None:
            raise ValidationError('Только буквы, цифры и @/./+/-/_.')
        if User.objects.filter(username=value).first():
            raise ValidationError('Этот username уже занят')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError('Этот email уже занят')
        return value

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]


class UsersMeSerializer(UsersSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
        read_only_fields = ['role']
