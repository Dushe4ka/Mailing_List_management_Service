from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )
    name = models.CharField(
        verbose_name='Ф.И.О',
        max_length=150,
        **NULLABLE
    )
    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=255,
        **NULLABLE
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.email}, {self.name}, {self.comment}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
