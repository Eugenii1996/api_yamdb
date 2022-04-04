from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through='TitlesGenres',
        through_fields=('title', 'genre'),
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category", blank=True, null=True
    )

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class TitlesGenres(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="title"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="genre",
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]

    def __str__(self):
        return self.title
