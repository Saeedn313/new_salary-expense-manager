from pydantic import BaseModel

class Cost(BaseModel):
    description: str
    amount: float
    id: int = None
