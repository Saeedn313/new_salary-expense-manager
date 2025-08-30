from config import DB_FILE
from .base_db import BaseDb
from models.costs import Cost

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


    def add_cost(self, cost: Cost):
        cursor = self.conn.cursor()
        columns = ["description", "amount"]
        cursor.execute(self.add(self.table_name, columns), (cost.description, cost.amount))
        cost.id = cursor.lastrowid
        self.conn.commit()
        return cost
    
    def get_all_costs(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()
        return rows
    
    def get_one_cost(self, cost_id):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "cost_id"), (cost_id,)).fetchone()
        return row
    
    def delete_cost(self, cost_id):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "cost_id"), (cost_id, ))

    def update_cost(self, cost):
        cursor = self.conn.cursor()
        columns = ["description", "amount"]
        cursor.execute(self.update(self.table_name, columns), (cost.description, cost.amount, cost.id))
