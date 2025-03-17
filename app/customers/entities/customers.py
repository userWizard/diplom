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
