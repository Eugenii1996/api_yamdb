from rest_framework import serializers, validators
from reviews.models import (
    Category, Genre, Title, TitlesGenres, Comment, Review
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=TitlesGenres.objects.all(),
                fields=('title', 'genre')
            )
        ]

    def validate_genre(self, value):
        if self.context['request'].genre == value:
            raise serializers.ValidationError(
                'Данный жанр уже выбран!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
