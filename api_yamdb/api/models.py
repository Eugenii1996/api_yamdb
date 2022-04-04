from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser
)
from django.db import models
from django.db.models import UniqueConstraint
import jwt

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField()
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
