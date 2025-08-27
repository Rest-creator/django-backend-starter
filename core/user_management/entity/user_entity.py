from dataclasses import dataclass

@dataclass
class UserEntity:
    id: str
    email: str
    employee_id: str
    first_name: str
    last_name: str
    contact_number: str
    role: str
    branch: str
    region: str
    is_active: bool
