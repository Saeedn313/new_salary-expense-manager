from pydantic import BaseModel

class Cost:
    def __init__(self, description: str, amount: float, id: int = None):
        self.description = description
        self.amount = amount
        self.id = id

class CostIn(BaseModel):
    description: str
    amount: float

class CostOut(CostIn):
    id: int = None
