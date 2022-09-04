from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'
ROLE_USER = 'user'


ROLES = [
    (ROLE_ADMIN, 'Администратор'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_USER, 'Пользователь'),
]


class CustomUserManager(UserManager):
    """
    Create and save a user with the given username, email, and password.
    """
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        if username == 'me':
            raise ValueError('"me" is invalid username.')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    REQUIRED_FIELDS = ('email', 'password')

    role = models.CharField(
        choices=ROLES,
        default='user',
        max_length=15,
        blank=False
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    objects = CustomUserManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
