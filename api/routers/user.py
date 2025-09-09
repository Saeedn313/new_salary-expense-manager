from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models.users import UserIn
from db.user_db import UserDb
import os



# tags is used for /docs in fastapi
router = APIRouter(prefix="/users", tags=["users"])
user_db = UserDb()
user_db.create_user_tables()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))


@router.get("/", response_class=HTMLResponse)
def get_all_users(request: Request):
    try:
        users = user_db.get_all_users()
        if len(users) < 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!")
        return templates.TemplateResponse("users.html", {"request": request, "users": users})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.get("/{user_id}", response_class=HTMLResponse)
def get_one_user(user_id: int, request: Request):
    try:
        user = user_db.get_one_user(user_id)
        if user == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no user found")
        return templates.TemplateResponse("user_profile.html", {"request": request, "user": user})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

@router.post('/add-user')
def add_new_user(user: UserIn):
    try:
        user_db.add_user(user.dict())
        return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post('/delete-user/{user_id}')
def delete_user(user_id: int):
    try:
        deleted = user_db.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found to delete!")
        return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)
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
        return RedirectResponse(url=f"/users/{user_id}")
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))