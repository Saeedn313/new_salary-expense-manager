from config import DB_FILE
from .base_db import BaseDb
from models.db_models.costs import Cost, CostOut

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
            "year": "INTEGER NOT NULL",
            "month": "INTEGER NOT NULL CHECK(month > 0 AND month <= 12)",
            "date": "TEXT DEFAULT CURRENT_TIMESTAMP"
            }
            cursor.execute(self.create_tables(self.table_name, cols))
            self.conn.commit()


    def add_cost(self, cost_dict: dict):
        cost = Cost(description=cost_dict["description"], amount=cost_dict["amount"], year=cost_dict["year"], month=cost_dict["month"])
        cursor = self.conn.cursor()
        columns = ["description", "amount", "year", "month"]
        cursor.execute(self.add(self.table_name, columns), (cost.description, cost.amount, cost.year, cost.month))
        cost.id = cursor.lastrowid
        self.conn.commit()
        return cost
    
    def get_all_costs(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()
        
        all_costs = []
        for row in rows:
            cost = Cost(description=row["description"], amount=row["amount"], year=row["year"], month=row["month"], id=row["cost_id"])
            all_costs.append(cost)
        print(all_costs)
        return all_costs
    
    def get_one_cost(self, cost_id: int):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "cost_id"), (cost_id,)).fetchone()
        
        cost = Cost(description=row["description"], amount=row["amount"], id=row["cost_id"], year=row["year"], month=row["month"])
        return cost if cost is not None else None
    
    def delete_cost(self, cost_id: int):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "cost_id"), (cost_id, ))
        self.conn.commit()

        return cursor.rowcount > 0

    def update_cost(self, cost_id: int, cost_dict: dict):
        cost = Cost(description=cost_dict["description"], amount=cost_dict["amount"], year=cost_dict["year"], month=cost_dict["month"], id=cost_id)

        cursor = self.conn.cursor()
        columns = ["description", "amount", "year", "month"]
        cursor.execute(self.update(self.table_name, columns, "cost_id"), (cost.description, cost.amount, cost.year, cost.month, cost.id))

        return cursor.rowcount > 0
