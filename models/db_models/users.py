from jdatetime import datetime


class User:
    def __init__(self, name: str, family: str, id: int = None, created_at = None):
        self.name = name
        self.family = family
        self.id = id
        self.created_at = created_at

    def full_name(self):
        return f"{self.name} {self.family}"
    
    def calc_salary(self, hourly_rate: float, total_hour: int, total_min: int) -> float:
        total_hours = (total_min / 60) + total_hour
        return round(total_hours * hourly_rate, 1)
    
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
    def __init__(self, name: str, family: str, id: int = None, created_at=None):
        super().__init__(name, family, id, created_at)
        self.role = "Developer"

class Manager(User):
    def __init__(self, name: str, family: str, id: int = None, created_at = None):
        super().__init__(name, family, id, created_at)
        self.role = "Manager"

