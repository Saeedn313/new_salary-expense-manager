from fastapi import APIRouter, HTTPException, status
from db.salary_db import SalaryDb
from models.api_models.salary_schema import SalaryIn
from db.user_db import UserDb
from models.db_models.users import User


router = APIRouter(prefix="/salaries", tags=["salaries"])
salary_db = SalaryDb()
user_db = UserDb()
salary_db.create_salary_tables()


@router.post('/add-salary')
def add_salary(salary: SalaryIn):
    try:
        print(salary.dict())
        user: User = user_db.get_one_user(user_id=salary.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        
        salary_exist = salary_db.get_salary(user_id=salary.user_id, year=salary.year, month=salary.month)
        if salary_exist is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Salary for {salary.year}-{salary.month} already exists for this user")
        
        user_salary = user.calc_salary(hourly_rate=salary.hourly_rate, total_hour=salary.total_hour, total_min=salary.total_min)
        salary_dict = {"user_id": salary.user_id, "year": salary.year, "month": salary.month, "hourly_rate": salary.hourly_rate, "total_min": salary.total_min, "total_hour": salary.total_hour, "total_salary": user_salary}
        new_salary = salary_db.add_salary(salary_dict=salary_dict)
        return {"detail": new_salary}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@router.post("/delete-salary/{salary_id}")
def delete_salary(salary_id: int):
    try:
        deleted = salary_db.delete_salary(salary_id=salary_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salary not found")
        return {"detail": f"Salary with id {salary_id} is deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")



@router.post("/update-salary/{salary_id}")
def update_salary(salary_id: int, salary: SalaryIn):
    try:
        user: User = user_db.get_one_user(user_id=salary.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        
        user_salary: float = user.calc_salary(hourly_rate=salary.hourly_rate, total_hour=salary.total_hour, total_min=salary.total_min)
        salary_dict = {"user_id": salary.user_id, "year": salary.year, "month": salary.month, "hourly_rate": salary.hourly_rate, "total_min": salary.total_min, "total_hour": salary.total_hour, "total_salary": user_salary}

        updated = salary_db.update_salary(salary_id=salary_id, salary_dict=salary_dict)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Salary with id {salary_id} not found")
        
        return {"detail": "salary_updated"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

        