import sqlite3
from config import DB_FILE



class UserDb:
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE, check_same_thread=False)

    def init_db(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                family TEXT,
                role TEXT
                )
            """)
            conn.commit()

    def add(self, user):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users (name, family, role, hourly_rate, total_hour, total_minute)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (user.name, user.family, user.role, user.hourly_rate,user.total_hour, user.total_minute))
            conn.commit()
            user.id = cursor.lastrowid
        return user

    def fetch_all(self):
        with self.connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("""
            SELECT * FROM users
            """).fetchall()
        return rows

    def fetch_one(self, user_id):
        with self.connection as conn:
            cursor = conn.cursor()
            row = cursor.execute("""
                SELECT * FROM users WHERE id=?
            """, (user_id,)).fetchone()

        return row
    
    def delete(self, user_id):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM users WHERE id=?
            """, (user_id,))

    def update(self, user):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE users SET name=?, family=?, role=?, hourly_rate=?,total_hour=?, total_minute=? WHERE id=?
            """, (user.name, user.family, user.role, user.hourly_rate,user.total_hour, user.total_minute, user.id))                             


