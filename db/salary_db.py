from config import DB_FILE
from .base_db import BaseDb
from models.api_models.salary_schema import SalaryOut
from jdatetime import datetime

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
            "FOREIGN KEY(user_id)": "REFERENCES users(user_id) ON DELETE CASCADE"
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
        if not rows:
            return None

        return [SalaryOut(user_id = row["user_id"],
            year = row["year"],
            month = row["month"],
            hourly_rate = row["hourly_rate"],
            total_min = row["total_min"],
            total_hour = row["total_hour"],
            total_salary = row["total_salary"],
            id = row["salary_id"]) for row in rows]   
        
    # def get_total_salary(self):
    #     cursor = self.conn.cursor()
    #     row = cursor.execute(f"SELECT SUM(amount) AS total_spend, AVG(amount) AS avrage_spend, MIN(amount) AS lowest_spend, MAX(amount) AS highest_spend FROM {self.table_name}").fetchone()
        
    #     return {
    #         "total_spend": row["total_spend"],
    #         "avrage_spend": row["avrage_spend"],
    #         "lowest_spend": row["lowest_spend"],
    #         "highest_spend": row["highest_spend"]
    #     }
    
    
    def get_salary_summery(self):
        cursor = self.conn.cursor()
        row = cursor.execute(f"SELECT SUM(total_salary) AS total_salary, SUM(total_hour) AS total_hour , AVG(hourly_rate) AS avg_hourly_rate, COUNT(*) AS total_record  FROM {self.table_name}").fetchone()
        
        return {
            "total_salary": row["total_salary"],
            "total_hour": row["total_hour"],
            "avg_hourly_rate": row["avg_hourly_rate"],
            "total_record": row["total_record"]
        }
        
 
    
    def get_salary_by_year_month(self, year: int, month: int):
        cursor = self.conn.cursor()
        rows = cursor.execute(
            """
            SELECT u.name, u.family, s.year, s.month, s.hourly_rate, s.total_salary
            FROM salaries AS s
            INNER JOIN users AS u ON u.user_id = s.user_id
            WHERE s.year = ? AND s.month = ?
            ORDER BY s.total_salary DESC
            """,
            (year, month)).fetchall()
        
        if not rows: 
            return None
        monthly_summery = [
            {"name": row["name"],
             "family":row["family"],
             "year": row["year"],
             "month": row["month"],
             "hourly_rate": row["hourly_rate"],
             "total_salary": row["total_salary"]
             } for row in rows
            ]
        return monthly_summery
    
    def get_salary_per_role(self):
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT u.role, SUM(s.total_salary) AS total_salary, AVG(s.hourly_rate) AS avg_hourly_rate, SUM(s.total_hour) AS total_hour FROM salaries AS s INNER JOIN users AS u on u.user_id = s.user_id GROUP BY u.role").fetchall()
        
        if not rows:
            return None
        summery_per_role = [
            {
                "role": row["role"],
                "total_salary": row["total_salary"],
                "avg_hourly_rate": row["avg_hourly_rate"],
                "total_hour": row["total_hour"]
            } for row in rows
        ]
        return summery_per_role
    
    
    def get_cost_within_year_month(self, start_year: int, end_year:int, start_month: int = None, end_month:int = None):
        cursor = self.conn.cursor()
        if start_month and end_month:
            rows = cursor.execute(f"SELECT year, month , SUM(total_salary) AS total_salary FROM {self.table_name} WHERE year BETWEEN ? AND ? AND month BETWEEN ? AND ? GROUP BY year, month ORDER BY year, month", (start_year, end_year, start_month, end_month)).fetchall()
        else:
            rows = cursor.execute(f"SELECT year, month , SUM(total_salary) AS total_salary FROM {self.table_name} WHERE year BETWEEN ? AND ? GROUP BY year, month ORDER BY year, month ",(start_year, end_year)).fetchall()
            
        if not rows:
            return None
        
        year_month_summery = [{"year": row["year"], "month": row["month"], "total_salary": row["total_salary"]} for row in rows]
        return year_month_summery  
    
    def get_last_month_salary(self):
        cursor = self.conn.cursor()
        this_year, this_month = (datetime.now().year, datetime.now().month)
        month_name = datetime.now().strftime("%B")
        row = cursor.execute("SELECT SUM(total_salary) AS total_salary, SUM(total_hour) AS total_hour , AVG(hourly_rate) AS avg_hourly_rate, COUNT(*) AS total_record FROM salaries WHERE year=? AND month=? GROUP BY year, month", (this_year, this_month)).fetchone()
        if not row:
            return None
        
        last_month_summary = {"total_salary": row["total_salary"], "total_hour": row["total_hour"], "avg_hourly_rate": row["avg_hourly_rate"], "total_record": row["total_record"], "month": month_name}
        return last_month_summary

