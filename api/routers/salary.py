from fastapi import APIRouter, HTTPException, status
from db.salary_db import SalaryDb


router = APIRouter(prefix="/salaries", tags=["salaries"])
salary_db = SalaryDb()
salary_db.create_salary_tables()



