from pydantic import BaseModel
class User:
    def __init__(self, name: str, family: str, id: int = None):
        self.name = name
        self.family = family
        self.id = id

    def full_name(self):
        return f"{self.name} {self.family}"
    
    def calc_salary(self) -> int:
        total_hours = (self.total_min / 60) + self.total_hour
        return int(total_hours * self.hourly_rate)
    
    # def get_all_users(rows: dict):
        
    #     all_users = []
    #     try:
    #         if rows is None:
    #             raise RuntimeError("no user found!")
    #         for row in rows:
    #             if row["role"] == "Developer":
    #                 user = Developer(name=row["name"], family=row["family"],id=row["user_id"])
    #             if row["role"] == "Manager":
    #                 user = Manager(name=row["name"], family=row["family"],id=row["user_id"])

    #             all_users.append(UserOut(name=user.name, family=user.family, role=user.role, id=user.id).dict())
    #         return all_users
    #     except Exception as e:
    #         raise RuntimeError(f"error in fetching users from db: {e}")

# def get_all_users_service():
#     all_users = []
#     try:
#         rows = user_db.get_all_users()
#         if rows is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no cost found!')
#         for row in rows:
#             user = User(name=row["name"], family=row["family"], role=row["role"], id=row["user_id"])
#             all_users.append(user.dict())
#         return all_users
#     except Exception as e:
#         raise RuntimeError(f"error in fetching users from db: {e}")


class Developer(User):
    def __init__(self, name: str, family: str, id: int = None):
        super().__init__(name, family, id)
        self.role = "Developer"

class Manager(User):
    def __init__(self, name: str, family: str, id: int = None):
        super().__init__(name, family, id)
        self.role = "Manager"


class UserIn(BaseModel):
    name: str
    family: str
    role: str

class UserOut(UserIn):
    id : int


# class Developer(User):
#     def __init__(self, name: str, family: str, id: int = None):
#         super().__init__(name, family, id)
#         self.role = "Developer"


# class Manager(User):
#     def __init__(self, name: str, family: str, id: int = None):
#         super().__init__(name, family, id)
#         self.role = "Manager"


# class Salary:
#     def __init__(
#         self,
#         description: str,
#         amount: float,
#         hourly_rate: float,
#         total_min: int,
#         total_hour: int,
#         id: int = None
#     ):
#         self.description = description
#         self.amount = amount
#         self.hourly_rate = hourly_rate
#         self.total_min = total_min
#         self.total_hour = total_hour
#         self.id = id

    