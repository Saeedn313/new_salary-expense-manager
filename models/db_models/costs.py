class Cost:
    def __init__(self, description: str, amount: float, year: int, month: int, id: int = None):
        self.description = description
        self.amount = amount
        self.year = year
        self.month = month
        self.id = id
        
    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "year": self.year,
            "month": self.month,
            "id": self.id
        }


