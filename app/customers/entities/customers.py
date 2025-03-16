from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    id: Optional[int] = field(default=None, kw_only=True)
    name: str
    email: str
    phone_number: str
    password: str
    created_at: datetime

@dataclass
class CustomerCreate:
    name: str
    email: str
    phone_number: str
    password: str

@dataclass
class CustomerUpdate:
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None