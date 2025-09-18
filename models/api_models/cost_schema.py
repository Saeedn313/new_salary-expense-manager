from pydantic import BaseModel

class CostIn(BaseModel):
    description: str
    amount: float
    year: int
    month: int

class CostOut(CostIn):
    id: int = None