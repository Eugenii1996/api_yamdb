import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = ('__all__',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Вы не можете добавить более'
                                  'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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

    class Meta:
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'confirmation_code',
        )


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для auth, users"""

    def validate_username(self, value):
        RegisterUserSerializer(self, value)
        return value

    def validate_email(self, value):
        RegisterUserSerializer(self, value)
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
        fields = UsersSerializer.Meta.fields
        read_only_fields = ['role']
