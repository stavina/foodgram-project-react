from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'

ROLE_CHOICES = (
    (USER_ROLE, 'Пользователь'),
    (MODERATOR_ROLE, 'Модератор'),
    (ADMIN_ROLE, 'Администратор'),
)

ROLE_LENGTH = 20
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
FIRST_NAME_LENGTH = 150
LAST_NAME_LENGTH = 150
PASSWORD_LENGTH = 150


class User(AbstractUser):
    """Пользователь проекта Foodgram"""

    role = models.CharField(
        verbose_name='Роль',
        max_length=ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        blank=True
    )
    email = models.EmailField(max_length=EMAIL_LENGTH, unique=True)
    username = models.CharField(
        db_index=True,
        max_length=USERNAME_LENGTH,
        unique=True,
        verbose_name="Логин",
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_LENGTH,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=LAST_NAME_LENGTH,
        verbose_name="Фамилия",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-username"]

    def __str__(self):
        """Строковое представление модели."""
        return self.username


class Subscription(models.Model):
    """Подписка пользователей друг на друга."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name="Автор рецепта",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Подписчик",
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = (
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='no_self_subscribe'
            ),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            )
        )

    def __str__(self):
        """Строковое представление модели."""
        return f"Пользователь {self.user}, подписан на  {self.author}"

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE

    @property
    def is_user(self):
        return self.role == USER_ROLE

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE
