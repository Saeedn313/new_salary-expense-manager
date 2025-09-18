from pydantic import BaseModel

class UserIn(BaseModel):
    name: str
    family: str
    role: str

class UserOut(UserIn):
    id : int
    created_at: str = None
