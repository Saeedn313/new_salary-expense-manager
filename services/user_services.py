from db.user_db import UserDb
from models.users import User

user_db = UserDb()
user_db.create_user_tables()

def get_all_users_service():
    all_users = []
    try:
        rows = user_db.get_all_users()
        for row in rows:
            user = User(name=row["name"], family=row["family"], role=row["role"], id=row["user_id"])
            all_users.append(user.dict())
        return all_users
    except Exception as e:
        raise RuntimeError(f"error in fetching users from db: {e}")
    
def add_user_service(user: User):
    try:
        return user_db.add_user(user)
    except Exception as e:
        raise RuntimeError(f"Error in adding user: {e}")

def delete_user_service(user_id: int):
    try:
        user_db.delete_user(user_id)
        return True
    except Exception as e:
        raise RuntimeError(f"Error deleting user: {e}")

def update_user_service(user_id: int, user: User):
    try:
        user.id = user_id
        user_db.update_user(user)
        return True
    except Exception as e:
        raise RuntimeError(f"Error updating user: {e}")