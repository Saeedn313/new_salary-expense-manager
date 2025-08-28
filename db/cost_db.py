from config import DB_FILE
from .base_db import BaseDb

class CostDb(BaseDb):
    def __init__(self):
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