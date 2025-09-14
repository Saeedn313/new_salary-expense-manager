from fastapi import APIRouter, HTTPException, status, Form
from db.salary_db import SalaryDb
from db.user_db import UserDb
from models.users import User


router = APIRouter(prefix="/salaries", tags=["salaries"])
salary_db = SalaryDb()
user_db = UserDb()
salary_db.create_salary_tables()


@router.post('/add-salary')
def add_salary(user_id: int = Form(...), year: int = Form(...), month: int = Form(...), hourly_rate: float = Form(...), total_min: int = Form(...), total_hour: int = Form(...)):
    user: User = user_db.get_one_user(user_id=user_id)
    salary = user.calc_salary(hourly_rate=hourly_rate, total_hour=total_hour, total_min=total_min)
    salary_dict = {"user_id": user_id, "year": year, "month": month, "hourly_rate": hourly_rate, "total_min": total_min, "total_hour": total_hour, "total_salary": salary}
    salary_db.add_salary(salary_dict=salary_dict)
    return {"detail": "salary_added"}

