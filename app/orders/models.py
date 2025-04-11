from django.db import models

from app.common.models import TimeBaseModel
from app.products.models.producst import Products
from app.project.settings import main as main_settings
from app.project.settings.main import AUTH_USER_MODEL

class Orders(TimeBaseModel):
    user = models.ForeignKey(
        main_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order'
    )