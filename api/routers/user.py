from fastapi import APIRouter, HTTPException
from services import user_services
from models.users import User

# tags is used for /docs in fastapi
router = APIRouter(prefix="/users", tags=["users"])


@router.get('/')
def get_all_users():
    try:
        users = user_services.get_all_users_service()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/add-user')
def add_new_user(user: User):
    try:
        new_user = user_services.add_user_service(user)
        return {"user": new_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete-user/{user_id}')
def delete_user(user_id: int):
    try:
        if user_services.delete_user_service(user_id):
            return {"detail": f"user with id: {user_id} is deleted!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-user/{user_id}")
def update_user(user_id: int, user: User):
    try:
        if user_services.update_user_service(user_id, user):
            return {"detail": f"user with id: {user_id} is updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))