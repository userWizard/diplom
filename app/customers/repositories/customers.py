from app.customers.services.customers import BaseCustomerService
from app.customers.services.auth import BaseAuthService
from app.customers.entities.customers import Customer as CustomersEntity
from app.customers.models.customers import Customer as CustomersModels
from app.customers.execeptions.customers import CustomerByIdInvalid

class ORMCustomerRepository(BaseCustomerService):
    
    def get_or_create(self, customer: CustomersEntity) -> CustomersEntity:
        customer, _ = CustomersModels.objects.get_or_create(
            customer=customer.name,
            customer=customer.email,
            customer=customer.phone_number,
            customer=customer.password,
        )
        
        return customer.to_entity()
    def get_by_id(self, user_id: int) -> CustomersEntity:
        try:
            customer = CustomersModels.object.get(user_id=user_id)
        except CustomersModels.DoesNotExist:
            raise CustomerByIdInvalid(user_id=user_id)
        
        return customer.to_entity()
    
    def authorize(self, email: str, password: str) -> CustomersEntity:
        ...
    
    def update_customer(self, email: str, password: str) -> CustomersEntity:
        ...
    
    def delete_account(self, user_id: int) -> CustomersEntity:
        try:
            customer = CustomersModels.object.get(user_id=user_id)
        except CustomersModels.DoesNotExist:
            raise None
        
        customer.delete()
        
        return customer.to_entity()


class ORMAuthRepository(BaseAuthService):
    ...