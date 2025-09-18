from pydantic import BaseModel

class SalaryIn(BaseModel):
    user_id: int
    year: int
    month: int
    hourly_rate: float
    total_min: int
    total_hour: int

class SalaryOut(SalaryIn):
    id: int
    total_salary: float
