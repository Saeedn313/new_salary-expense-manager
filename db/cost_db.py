from config import DB_FILE
from .base_db import BaseDb
from models.costs import Cost, CostOut

class CostDb(BaseDb):
    def __init__(self):
        super().__init__()
        self.table_name = "costs"

    def create_cost_tables(self):
            cursor = self.conn.cursor()
            cols = {
            "cost_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "description": "TEXT NULL",
            "amount": "REAL NOT NULL",
            "date": "TEXT DEFAULT CURRENT_TIMESTAMP"
            }
            cursor.execute(self.create_tables(self.table_name, cols))
            self.conn.commit()


    def add_cost(self, cost_dict: dict):
        cost = Cost(description=cost_dict["description"], amount=cost_dict["amount"])
        cursor = self.conn.cursor()
        columns = ["description", "amount"]
        cursor.execute(self.add(self.table_name, columns), (cost.description, cost.amount))
        cost.id = cursor.lastrowid
        self.conn.commit()
        return CostOut(description=cost.description, amount=cost.amount, id=cost.id)
    
    def get_all_costs(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()
        
        all_costs = []
        for row in rows:
            cost = Cost(description=row["description"], amount=row["amount"], id=row["cost_id"])
            all_costs.append(CostOut(description=cost.description, amount=cost.amount, id=cost.id))
        return all_costs
    
    def get_one_cost(self, cost_id: int):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "cost_id"), (cost_id,)).fetchone()
        
        cost = Cost(description=row["description"], amount=row["amount"], id=row["cost_id"])
        return CostOut(description=cost.description, amount=cost.amount, id=cost.id) if cost is not None else None
    
    def delete_cost(self, cost_id: int):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "cost_id"), (cost_id, ))
        self.conn.commit()

        return cursor.rowcount > 0

    def update_cost(self, cost_id: int, cost_dict: dict):
        cost = Cost(description=cost_dict["description"], amount=cost_dict["amount"], id=cost_id)

        cursor = self.conn.cursor()
        columns = ["description", "amount"]
        cursor.execute(self.update(self.table_name, columns, "cost_id"), (cost.description, cost.amount, cost.id))

        return cursor.rowcount > 0
