from .base_db import BaseDb

class Salary(BaseDb):
    def __init__(self):
        super().__init__()
        self.table_name = "salaries"

    def create_salary_tables(self):
        cursor = self.conn.cursor()
        cols = {
            "salary_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "year": "INTEGER NOT NULL",
            "month": "INTEGER NOT NULL",
            "hourly_rate": "REAL NOT NULL",
            "total_min": "INTEGER NOT NULL",
            "total_hour": "REAL NOT NULL",
            "total_salary": "REAL NOT NULL",
            "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP"
        }
        cursor.execute(self.create_tables(self.table_name, cols))
        self.conn.commit()

    def add_salary(self, salary):
        cursor = self.conn.cursor()
        cols = ["year", "month", "total_min", "total_hour", "total_salary"]
        cursor.execute(self.add(self.table_name, cols) (salary.year, salary.month, salary.hourly_rate, salary.total_min, salary.total_hour, salary.total_salary))
        salary.id = cursor.lastrowid
        return salary
    
    def get_all_salaries(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()
        return rows
    
    def get_one_salary(self):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name)).fetchone()
        return row
    
    def delete_salary(self, salary_id):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "salary_id"), (salary_id, ))

    def upadte_salary(self, salary):
        cursor = self.conn.cursor()
        cols = ["year", "month", "total_min", "total_hour", "total_salary"]
        cursor.execute(self.update(self.table_name, cols), (salary.year, salary.month, salary.hourly_rate, salary.total_min, salary.total_hour, salary.total_salary))
    
