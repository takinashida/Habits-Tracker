from django.db import models

from users.models import User


# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )

    time = models.TimeField(
        verbose_name='Время выполнения'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name='Связанная привычка'
    )

    period = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )

    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )

    duration = models.PositiveSmallIntegerField(
        verbose_name='Время выполнения (в секундах)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f'{self.action} ({self.user})'