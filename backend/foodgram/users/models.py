from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    sub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )
