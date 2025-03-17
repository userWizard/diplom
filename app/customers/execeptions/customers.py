from dataclasses import dataclass
from exceptions import ServiceException

@dataclass(eq=False)
class CustomerByIdInvalid(ServiceException):
    user_id : int
    
    @property
    def message(self):
        return 'Customer with id {user_id} not found'

@dataclass(eq=False)
class CustomerUpdateInvalid(ServiceException):
    user_id : int
    
    @property
    def message(self):
        return 'Customer with id {user_id} not found'