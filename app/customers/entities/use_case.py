from abc import (
    ABC,
    abstractmethod,
)

from app.customers.entities.services import BaseCustomerService
from app.customers.entities.entities import Customer

class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    @abstractmethod
    async def authorize(self, email: str, password: str) -> Customer:
        """Авторизовать пользователя."""
        ...

    @abstractmethod
    async def delete_account(self, user_id: int) -> None:
        """Выйти из системы."""
        ...

class AuthService(BaseAuthService):
    def authorize(self, email: str, password: str):
        customer = self.customer_service.authorize(email, password)
        
    def logout(self, user_id: int):
        customer = self.customer_service.logout(user_id)