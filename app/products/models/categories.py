from django.db import models

from app.common.models import TimeBaseModel

class Categories(TimeBaseModel):
    title = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

