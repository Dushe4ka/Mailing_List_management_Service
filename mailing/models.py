from django.db import models
from django.utils import timezone

from client.models import Client
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    theme = models.CharField(
        max_length=150,
        verbose_name='Тема письма',
        **NULLABLE
    )
    content = models.TextField(
        verbose_name='Содержание письма',
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.theme} - {self.creator}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingParameters(models.Model):
    intervals = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )
    status_variants = (
        ('is_active', 'Активен'),
        ('not_active', 'Неактивен'),
        ('finished', 'закончен успешно'),
        ('finished_date', 'закончен в срок'),
        ('finished_error', 'закончен с ошибками')
    )
    name = models.CharField(
        max_length=150,
        verbose_name='Название рассылки',
        default='mailing_no_name'
    )
    client = models.ManyToManyField(
        Client,
        verbose_name='Получатель',
    )
    mail = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Тема письма',
    )
    start_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='начало рассылки'
    )
    end_time = models.DateTimeField(
        default=(timezone.now() + timezone.timedelta(days=1)),
        verbose_name='конец рассылки'
    )
    next_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата следующей рассылки'
    )
    interval = models.CharField(
        max_length=50,
        choices=intervals,
        verbose_name='Интервал рассылки',
        default='daily'
    )
    status = models.CharField(
        max_length=50,
        choices=status_variants,
        verbose_name='Статус рассылки',
        default='not_active'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель',
        **NULLABLE
    )

    def __str__(self):
        return (f'{self.name}: ({self.start_time} - {self.end_time};интервал:{self.interval};'
                f' статус:{self.status}), creator:{self.creator}')

    class Meta:
        verbose_name = 'Параметры рассылки'
        verbose_name_plural = 'Параметры рассылок'
        permissions = [
            ('change_status', 'Can change status')
        ]


class Logs(models.Model):
    mailing = models.ForeignKey(
        MailingParameters,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
    )
    last_time_sending = models.DateTimeField(
        auto_now=True,
        verbose_name='время последней рассылки',
        **NULLABLE
    )
    status = models.CharField(
        max_length=50,
        verbose_name='Статус рассылки',
        **NULLABLE
    )
    response = models.CharField(
        max_length=200,
        verbose_name='Ответ почтового сервера',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'

    def __str__(self):
        return f'''Отправлено: {self.last_time_sending},
                  'Статус: {self.status} ,
                  'Response: {self.response},
                  'Mailing_parameters: {self.mailing}'''
