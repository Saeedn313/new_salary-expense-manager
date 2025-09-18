from fastapi import APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
from models.api_models.user_schema import UserIn, UserOut
from db.user_db import UserDb
from db.salary_db import SalaryDb
import os



# tags is used for /docs in fastapi
router = APIRouter(prefix="/users", tags=["users"])
user_db = UserDb()
salary_db = SalaryDb()
user_db.create_user_tables()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))


@router.get("/")
def get_all_users():
    try:
        users = user_db.get_all_users()
        if len(users) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")
        
        users_out = [UserOut(**user.to_dict()) for user in users]
        return {"users": users_out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/{user_id}")
def get_one_user(user_id: int):
    try:
        user = user_db.get_one_user(user_id)
        if user == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no user found")

        user_out = UserOut(**user.to_dict())
        return {"user": user_out}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post('/add-user')
def add_new_user(user: UserIn):

    try:
        new_user = user_db.add_user(user.dict())
        user_out = UserOut(**new_user.to_dict())
        return {"user": user_out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post('/delete-user/{user_id}')
def delete_user(user_id: int):
    try:
        deleted = user_db.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to delete!")
        return {"message": f"User with id {user_id} is deleted!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post("/update-user/{user_id}")
def update_user(user_id: int, user: UserIn):
    try:
        updated = user_db.update_user(user_id, user.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to update!")
        return {"message": "User with id {user_id} is updated!"}
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))