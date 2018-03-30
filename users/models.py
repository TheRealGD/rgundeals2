from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .validators import UsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom model to replace Django's stock User. Omits fields we don't need, like first_name and last_name.
    """
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text="Letters, digits and @/./+/-/_ only (30 characters max)",
        validators=[UsernameValidator()],
        error_messages={
            'unique': "A user with that username already exists.",
        }
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Has administrative access",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Can log in",
    )
    date_joined = models.DateTimeField(
        default=timezone.now
    )
    vendor = models.ForeignKey(
        to='deals.vendor',
        related_name='users',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:user', kwargs={'username': self.username})

    def clean(self):
        super().clean()

        # Convert email to lowercase
        self.email = self.email.lower()
