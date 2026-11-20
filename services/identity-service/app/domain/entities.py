from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    CLIENT = "CLIENT"
    MECHANIC = "MECHANIC"
    ADMIN = "ADMIN"

@dataclass
class User:
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool
    created_at: datetime