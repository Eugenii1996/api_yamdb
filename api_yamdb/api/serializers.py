from rest_framework import serializers, validators

from reviews.models import Category, Genre, Title, TitlesGenres


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
