from django.db import models

from app.common.models import TimeBaseModel
from app.customers.entities.customers import Customer

class Customers(TimeBaseModel):
    '''Customers model'''
    name = models.CharField(
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
        max_length=30,
        blank=False,
        null=False,
    )
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self) -> str:
        return f'{self.firstname}:{self.secondname}:{self.email}:{self.phone_number}'
    
    def to_entity(self) -> Customer:
        return Customer(
            id=self.pk,
            name=self.name,
            email=self.email,
            phone_number=self.phone_number,
            password=self.password,
            created_at=self.created_at,
        )
    