from config import DB_FILE
from .base_db import BaseDb
from models.db_models.costs import Cost
from jdatetime import datetime

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
        return all_costs
    
    def get_one_cost(self, cost_id: int):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "cost_id"), (cost_id,)).fetchone()
        if not row:
            return None
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
    
    def get_costs_summery(self):
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT COUNT(*) AS total_costs, SUM(amount) AS total_spend, AVG(amount) AS avrage_spend, MIN(amount) AS lowest_spend, MAX(amount) AS highest_spend FROM {self.table_name}").fetchone()
        
        return {
            "total_costs": row["total_costs"],
            "total_spend": row["total_spend"],
            "avrage_spend": row["avrage_spend"],
            "lowest_spend": row["lowest_spend"],
            "highest_spend": row["highest_spend"]
        }
        
    def get_costs_by_year(self, year: int):
        cursor = self.conn.cursor()
        rows = cursor.execute(f"SELECT year, SUM(amount) AS total_spend FROM {self.table_name} WHERE year=? GROUP BY year ORDER BY year DESC", (year,)).fetchall()
        
        year_summery = [{"year": row["year"], "total_spend": row["total_spend"]} for row in rows]
        
        return year_summery
    
    def get_cost_by_year_month(self, year:int, month:int ):
        cursor = self.conn.cursor()
        rows = cursor.execute(f"SELECT year, month, amount FROM {self.table_name} WHERE year=? AND month=? ORDER BY month DESC", (year, month)).fetchall()
        
        if not rows:
            return None
        
        month_summery = [{"year": row["year"], "month": row["month"], "amount": row["amount"]} for row in rows]
        return month_summery
    
    def get_cost_within_year_month(self, start_year: int, end_year:int, start_month: int = None, end_month:int = None):
        cursor = self.conn.cursor()
        if start_month and end_month:
            rows = cursor.execute(f"SELECT year, month , SUM(amount) AS total_spend FROM {self.table_name} WHERE year BETWEEN ? AND ? AND month BETWEEN ? AND ? GROUP BY year, month ORDER BY year, month", (start_year, end_year, start_month, end_month)).fetchall()
        else:
            rows = cursor.execute(f"SELECT year, month , SUM(amount) AS total_spend FROM {self.table_name} WHERE year BETWEEN ? AND ? GROUP BY year, month ORDER BY year, month",(start_year, end_year)).fetchall()
        year_month_summery = [{"year": row["year"], "month": row["month"], "total_spend": row["total_spend"]} for row in rows]
        print(year_month_summery, rows)
        if not rows:
            return None
        return year_month_summery  
    
    def get_avg_month_year(self, year: int, month: int):
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT year, month, AVG(amount) avg_spend FROM costs WHERE year=? AND month=?", (year, month)).fetchone()
        
        if row["year"] == None or row["month"] == None:
            return None
        
        month_avg = {"year": row["year"], "month": row["month"], "avg_spend": row["avg_spend"]}
        return month_avg
    
    def get_last_month_summary(self):
        cursor = self.conn.cursor()
        this_year, this_month = (datetime.now().year, datetime.now().month)
        month_name = datetime.now().strftime("%B")
        row = cursor.execute("SELECT COUNT(*) AS total_costs, SUM(amount) AS total_spend, AVG(amount) AS avrage_spend, MIN(amount) AS lowest_spend, MAX(amount) AS highest_spend, month FROM costs WHERE year=? AND month=? GROUP BY year, month", (this_year,this_month)).fetchone()
        if not row:
            return None
        last_month_summary = {"total_costs": row["total_costs"], "total_spend": row["total_spend"], "avrage_spend": row["avrage_spend"], "lowest_spend": row["lowest_spend"], "highest_spend": row["highest_spend"], "month": month_name}
        return last_month_summary
            