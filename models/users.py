from pydantic import BaseModel

class User(BaseModel):
    name: str
    family: str 
    role: str
    id: int = None
        
    def full_name(self) -> str:
        return f"{self.name} {self.family}"
    


# class Developer(User):
#     def __init__(self, name: str, family: str, id: int = None):
#         super().__init__(name, family, id)
#         self.role = "Developer"


# class Manager(User):
#     def __init__(self, name: str, family: str, id: int = None):
#         super().__init__(name, family, id)
#         self.role = "Manager"


class Salary:
    def __init__(
        self,
        description: str,
        amount: float,
        hourly_rate: float,
        total_min: int,
        total_hour: int,
        id: int = None
    ):
        self.description = description
        self.amount = amount
        self.hourly_rate = hourly_rate
        self.total_min = total_min
        self.total_hour = total_hour
        self.id = id

    def calc_salary(self) -> int:
        total_hours = (self.total_min / 60) + self.total_hour
        return int(total_hours * self.hourly_rate)