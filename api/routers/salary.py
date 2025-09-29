from fastapi import APIRouter, HTTPException, status
from db.salary_db import SalaryDb
from models.api_models.salary_schema import SalaryIn
from db.user_db import UserDb
from models.db_models.users import User


router = APIRouter(prefix="/api/salaries", tags=["salaries"])
salary_db = SalaryDb()
user_db = UserDb()
salary_db.create_salary_tables()

@router.get("/summery")
def get_salary_summery():

        salaries_summery = salary_db.get_last_month_salary()
        salary_per_role = salary_db.get_salary_per_role()
        summery_data = {"salaries_summery": salaries_summery, "salary_per_role": salary_per_role}
        return summery_data

    
@router.get("/monthly-range")
def filter_salary(start_year: int, end_year: int, start_month:int = None, end_month: int = None):
    try:
        if start_month and not end_month or not start_month and end_month:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start and end month both should be specified!")
        filtered_costs = salary_db.get_cost_within_year_month(start_year, end_year, start_month, end_month)
        
        if filtered_costs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found!")
        return {"data": filtered_costs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@router.get("/monthly-salaries")
def get_salary_by_year_month(year: int, month: int):
    try:
        salary_per_month = salary_db.get_salary_by_year_month(year, month)
        if salary_per_month is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No result found!")
        return salary_per_month
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")



@router.post('/add-salary')
def add_salary(salary: SalaryIn):
    try:
        print(salary.dict())
        user: User = user_db.get_one_user(user_id=salary.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {salary.user_id} not found")
        
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
    
@router.get("/{user_id}")
def get_user_salary(user_id: int):
    try:
        user: User = user_db.get_one_user(user_id)
        # print(user)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_salaries = salary_db.get_user_all_salary(user_id)
        if user_salaries is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No salary found!")
        
        return {"salaries": user_salaries}
    
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
    
    
    

        