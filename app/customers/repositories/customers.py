from app.customers.services.customers import BaseCustomerService
from app.customers.services.auth import BaseAuthService

class ORMCustomerRepository(BaseCustomerService):
    ...


class ORMAuthRepository(BaseAuthService):
    ...