from app.customers.entities.services import BaseCustomerService
from app.customers.entities.use_case import BaseAuthService
from app.customers.entities.entities import Customer as CustomerEntity
from app.customers.models import Customers as CustomerModels
from app.customers.execeptions.customers import CustomerByIdInvalid


class ORMCustomerRepository(BaseCustomerService):
    
    def get_or_create(self, customer: CustomerEntity) -> CustomerEntity:
        db_customer, _ = CustomerModels.objects.get_or_create(
            customer=customer.name,
            customer=customer.email,
            customer=customer.phone_number,
            customer=customer.password,
        )
        
        return db_customer.to_entity()

    def get_by_id(self, user_id: int) -> CustomerEntity:
        try:
            db_customer = CustomerModels.objects.get(user_id=user_id)
        except CustomerModels.DoesNotExist:
            raise CustomerByIdInvalid(user_id=user_id)
        
        return db_customer.to_entity()
    
    def delete_customer(self, user_id: int) -> CustomerEntity:
        try:
            db_customer = CustomerModels.objects.filter(user_id=user_id)
        except CustomerModels.DoesNotExist:
            raise None
        
        db_customer.delete()
        
        return db_customer.to_entity()

    def update_customer(self, customer: CustomerEntity):
        db_customer = CustomerModels.objects.filter(id=customer.id).first()
        if db_customer:
            db_customer.email = customer.email
            db_customer.password = customer.password
            db_customer.save()
            db_customer.to_entity()

        return None
