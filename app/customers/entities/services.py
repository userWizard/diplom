from abc import ABC, abstractmethod
from app.customers.entities.entities import Customer as CustomerEntity

class BaseCustomerService(ABC):
    @abstractmethod
    async def get_or_create(self, customer: CustomerEntity) -> CustomerEntity:
        """Создать или получить пользователя."""
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> CustomerEntity:
        """Получить пользователя по ID."""
        ...

    @abstractmethod
    async def update_customer(self, email: str, password: str) -> CustomerEntity:
        """Обновить данные пользователя."""
        ...
    
    @abstractmethod
    def authorize(self, customer: CustomerEntity) -> CustomerEntity:
        """Авторизовать пользователя."""
        ...
    
    @abstractmethod
    def delete_account(self, user_id: int) -> CustomerEntity:
        """Выйти из системы."""
        ...