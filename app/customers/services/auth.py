from abc import (
    ABC,
    abstractmethod,
)

from dataclasses import dataclass

from app.customers.services.customers import BaseCustomerService
from app.customers.entities.customers import Customer

from abc import ABC, abstractmethod
from app.customers.entities.customers import Customer

class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    @abstractmethod
    async def authorize(self, email: str, password: str) -> Customer:
        """Авторизовать пользователя."""
        ...

    @abstractmethod
    async def logout(self, user_id: int) -> None:
        """Выйти из системы."""
        ...

class AuthService(BaseAuthService):
    def authorize(self, email: str, password: str):
        customer = self.customer_service.authorize(email, password)
        
    def logout(self, user_id: int):
        customer = self.customer_service.logout(user_id)