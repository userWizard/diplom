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
    def delete_customer(self, user_id: int) -> CustomerEntity:
        """Удалить аккаунт."""
        ...
    
    @abstractmethod
    def update_customer(self, customer: CustomerEntity) -> CustomerEntity:
        """Изменить данные из аккаунта."""
        ...