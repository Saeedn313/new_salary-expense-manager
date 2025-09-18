from config import DB_FILE
from .base_db import BaseDb
from models.api_models.salary_schema import SalaryOut

# assuming there is no base model for salary. 
# there is only pydantic models to be passed to fastapi.

class SalaryDb(BaseDb):
    def __init__(self):
        super().__init__()
        self.table_name = "salaries"

    def create_salary_tables(self):
        cursor = self.conn.cursor()
        cols = {
            "salary_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "user_id": "INTEGER NOT NULL",
            "year": "INTEGER NOT NULL",
            "month": "INTEGER NOT NULL",
            "hourly_rate": "REAL NOT NULL",
            "total_min": "INTEGER NOT NULL",
            "total_hour": "REAL NOT NULL",
            "total_salary": "REAL NOT NULL",
            "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
            "FOREIGN KEY(user_id)": "REFERENCES users(user_id)"
        }
        cursor.execute(self.create_tables(self.table_name, cols))
        self.conn.commit()

    def add_salary(self, salary_dict: dict):
        cursor = self.conn.cursor()
        columns = ["user_id", "year", "month", "hourly_rate", "total_min", "total_hour", "total_salary"]
        cursor.execute(
            self.add(self.table_name, columns),
            (
                salary_dict["user_id"],
                salary_dict["year"],
                salary_dict["month"],
                salary_dict["hourly_rate"],
                salary_dict["total_min"],
                salary_dict["total_hour"],
                salary_dict["total_salary"]
            )
        )
        salary_id = cursor.lastrowid
        self.conn.commit()

        return SalaryOut(id=salary_id, **salary_dict)

    def get_all_salaries(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()

        all_salaries = []
        for row in rows:
            all_salaries.append(
                SalaryOut(
                    id=row["salary_id"],
                    user_id=row["user_id"],
                    year=row["year"],
                    month=row["month"],
                    hourly_rate=row["hourly_rate"],
                    total_min=row["total_min"],
                    total_hour=row["total_hour"],
                    total_salary=row["total_salary"]
                ).dict()
            )

        return all_salaries

    def get_one_salary(self, salary_id: int):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "salary_id"), (salary_id,)).fetchone()

        if not row:
            return None

        return SalaryOut(
            id=row["salary_id"],
            user_id=row["user_id"],
            year=row["year"],
            month=row["month"],
            hourly_rate=row["hourly_rate"],
            total_min=row["total_min"],
            total_hour=row["total_hour"],
            total_salary=row["total_salary"]
        )

    def delete_salary(self, salary_id: int):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "salary_id"), (salary_id,))
        self.conn.commit()

        return cursor.rowcount > 0

    def update_salary(self, salary_id: int, salary_dict: dict):
        cursor = self.conn.cursor()
        columns = ["user_id", "year", "month", "hourly_rate", "total_min", "total_hour", "total_salary"]
        cursor.execute(
            self.update(self.table_name, columns, "salary_id"),
            (
                salary_dict["user_id"],
                salary_dict["year"],
                salary_dict["month"],
                salary_dict["hourly_rate"],
                salary_dict["total_min"],
                salary_dict["total_hour"],
                salary_dict["total_salary"],
                salary_id
            )
        )
        self.conn.commit()

        return cursor.rowcount > 0

    def get_latest_salary(self, user_id: int):
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id=?", (user_id,)).fetchone()
        return row["total_salary"] if row else None
    
    def get_salary_by_year_month(self, user_id, year, month):
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id=? year=? month=?", (user_id, year, month))

        return (row['total_salary'], row['year'], row['month'])

    def get_salary(self, user_id: int, year: int = None, month: int = None):
        cursor = self.conn.cursor()
        
        if year is not None and month is not None:
            row = cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE user_id=? AND year=? AND month=?"
                , (user_id, year, month)
                ).fetchone()
        else:
            row = cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE user_id=? ORDER BY year DESC, month DESC LIMIT 1"
                , (user_id)
                ).fetchone()
            
        if row is None:
            return None

        return SalaryOut(
            user_id = row["user_id"],
            year = row["year"],
            month = row["month"],
            hourly_rate = row["hourly_rate"],
            total_min = row["total_min"],
            total_hour = row["total_hour"],
            total_salary = row["total_salary"],
            id = row["salary_id"]
        )

    def get_user_all_salary(self, user_id):
        cursor = self.conn.cursor()
        rows = cursor.execute(f"SELECT * FROM {self.table_name} WHERE user_id=?", (user_id,)).fetchall()
        if rows is None:
            return None

        return [SalaryOut(user_id = row["user_id"],
            year = row["year"],
            month = row["month"],
            hourly_rate = row["hourly_rate"],
            total_min = row["total_min"],
            total_hour = row["total_hour"],
            total_salary = row["total_salary"],
            id = row["salary_id"]) for row in rows]   
        

