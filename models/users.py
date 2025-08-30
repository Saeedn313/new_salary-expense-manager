from pydantic import BaseModel

class User(BaseModel):
    name : str
    family: str
    id: int = None
        
    def full_name(self):
        return f'{self.name} {self.family}'

           
class Developer(User):
    role: str = "Developer"


class Manager(User):
    role: str = "Manager"


class Salary(BaseModel):
    description: str
    amount: float
    hourly_rate: float
    total_min: int
    total_hour: int
    id: int = None

    def calc_salary(self):
        total_hour = (self.total_min / 60) + self.total_hour
        salary = int(total_hour * self.hourly_rate)
        return salary



