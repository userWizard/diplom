from abc import ABC, abstractmethod
from app.customers.entities.customers import Customer, CustomerCreate, CustomerUpdate

class BaseCustomerService(ABC):
    @abstractmethod
    async def get_or_create(self, customer: CustomerCreate) -> Customer:
        """Создать или получить пользователя."""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Customer:
        """Получить пользователя по ID."""
        ...

    @abstractmethod
    async def update_customer(self, customer: CustomerUpdate) -> Customer:
        """Обновить данные пользователя."""
        ...