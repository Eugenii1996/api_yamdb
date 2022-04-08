from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
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
                            default='user',
                            blank=True,
                            null=False)
    confirmation_code = models.TextField()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        constraints = [UniqueConstraint(fields=['username', 'email'],
                                        name='unique_booking')]
        ordering = ['id']
