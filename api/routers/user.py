from fastapi import APIRouter, HTTPException, status, Body
# from services import user_services
from models.users import User, UserIn
from db.user_db import UserDb



# tags is used for /docs in fastapi
router = APIRouter(prefix="/users", tags=["users"])
user_db = UserDb()
user_db.create_user_tables()


@router.get('/')
def get_all_users():
    try:
        users = user_db.get_all_users()
        if len(users) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post('/add-user')
def add_new_user(user: UserIn):
    try:
        new_user = user_db.add_user(user.dict())
        return {"user": new_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.delete('/delete-user/{user_id}')
def delete_user(user_id: int):
    try:
        deleted = user_db.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to delete!")
        return {"detail": f"user with id: {user_id} is deleted!"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.put("/update-user/{user_id}")
def update_user(user_id: int, user: UserIn):
    try:
        updated = user_db.update_user(user_id, user.dict())
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to update!")
        return {"detail": f"user with id: {user_id} is updated!"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))