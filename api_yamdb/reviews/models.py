from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .validators import validate_year


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, )
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150,
                                  blank=True,
                                  null=True)
    last_name = models.CharField(max_length=150,
                                 blank=True,
                                 null=True)
    bio = models.TextField(blank=True,
                           null=True)
    role = models.TextField(choices=settings.ROLE_CHOICES,
                            default=settings.USER,
                            blank=True,
                            null=False)
    confirmation_code = models.TextField()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def is_admin(self):
        return (self.role == settings.ADMIN
                or self.is_superuser or self.is_staff)

    def is_moderator(self):
        return self.role == settings.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        constraints = [UniqueConstraint(fields=['username', 'email'],
                                        name='unique_booking')]
        ordering = ['username']


class CategoryGenre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Category(CategoryGenre):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(CategoryGenre):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    class Meta:
        ordering = ['-year', 'category', 'name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class ReviewComment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        related_query_name='%(class)s'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['pub_date']


class Review(ReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        default=0,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
