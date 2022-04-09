import datetime as dt
from rest_framework import serializers, validators

from reviews.models import (
    Category, Genre, Title, GenreTitle, Comment, Review
)
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=GenreTitle.objects.all(),
                fields=('title', 'genre')
            )
        ]

    def get_rating(self, obj):
        review = Review.objects.filter(title_id=obj.id)
        sum_rating = 0
        review_count = len(review)
        for i in review:
            sum_rating += i.rating
        return int(sum_rating/review_count)


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_genre(self, value):
        if self.context['request'].genre == value:
            raise serializers.ValidationError(
                'Данный жанр уже выбран!')
        return value
    
    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год создания произведения указан в будущем!'
            )
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
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'reviews']
            ),
        )


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
