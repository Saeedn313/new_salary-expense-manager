from pydantic import BaseModel
from datetime import datetime

class User:
    def __init__(self, name: str, family: str, id: int = None):
        self.name = name
        self.family = family
        self.id = id
        self.created_at = datetime.now().strftime("%I:%M%p on %B %d, %Y")

    def full_name(self):
        return f"{self.name} {self.family}"
    
    def calc_salary(self, hourly_rate: float, total_hour: int, total_min: int) -> int:
        total_hours = (total_min / 60) + total_hour
        return int(total_hours * hourly_rate)
    
    def to_dict(self):
        return {
            "name": self.name,
            "family": self.family,
            "id": self.id,
            "role": getattr(self, "role", None),
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<{self.id}> {self.name} {self.family} {self.created_at}"


class Developer(User):
    def __init__(self, name: str, family: str, id: int = None):
        super().__init__(name, family, id)
        self.role = "Developer"

class Manager(User):
    def __init__(self, name: str, family: str, id: int = None):
        super().__init__(name, family, id)
        self.role = "Manager"


class UserIn(BaseModel):
    name: str
    family: str
    role: str

class UserOut(UserIn):
    id : int
    created_at: str = None



# salary pydantic models

class SalaryIn(BaseModel):
    user_id: int
    year: int
    month: int
    hourly_rate: float
    total_min: int
    total_hour: float
    total_salary: float

class SalaryOut(SalaryIn):
    id: int



# class Salary:
#     def __init__(
#         self,
#         description: str,
#         amount: float,
#         hourly_rate: float,
#         total_min: int,
#         total_hour: int,
#         id: int = None
#     ):
#         self.description = description
#         self.amount = amount
#         self.hourly_rate = hourly_rate
#         self.total_min = total_min
#         self.total_hour = total_hour
#         self.id = id

    