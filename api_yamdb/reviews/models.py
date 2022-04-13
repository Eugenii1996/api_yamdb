from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


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
                            default=settings.ROLE_CHOICES[0][0],
                            blank=True,
                            null=False)
    confirmation_code = models.TextField()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def is_admin(self):
        if (self.role == settings.ROLE_CHOICES[2][0] or
                self.is_superuser):
            return True
        return False

    def is_moderator(self):
        if (self.role == settings.ROLE_CHOICES[1][0] or
                self.is_superuser):
            return True
        return False

    def __str__(self):
        return self.username

    class Meta:
        constraints = [UniqueConstraint(fields=['username', 'email'],
                                        name='unique_booking')]
        ordering = ['username']


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
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['pub_date']
