from django.db import models

from app.common.models import TimeBaseModel

class Customers(TimeBaseModel):
    '''Customers model'''
    username = models.CharField(
        verbose_name='Имя',
        max_length=90,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=55,
        unique=True,
    )
    phone_number = models.CharField(
        verbose_name='Телефон',
        max_length=20,
        unique=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        blank=False,
        null=False,
    )
    
    class Meta:
        ordering = ('username',)
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self) -> str:
        return f'{self.email}:{self.phone_number}'
