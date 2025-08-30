import sqlite3
from config import DB_FILE

class BaseDb:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def create_tables(self, table_name: str, columns: dict):
        sql_columns = ''
        for ind, (name, attr) in enumerate(columns.items()):
            if ind < len(columns) - 1:
                sql_columns += f'    {name} {attr},\n'
            else:
                sql_columns += f'    {name} {attr}'
        
        command = f"CREATE TABLE IF NOT EXISTS {table_name}(\n{sql_columns}\n)"
        return command
    
    def add(self, table_name: str, columns: list):
        sql_columns = ", ".join(columns)
        placeholders = ", ".join("?" for _ in range(columns))
        command = f"INSERT INTO {table_name} ({sql_columns}) VALUES ({placeholders})"
        return command

    def fetch_all(self, table_name):
        command = f"SELECT * FROM {table_name}"
        return command

    def fetch_one(self, table_name, col):
        command = f"SELECT * FROM {table_name} WHERE {col}=?"
        return command    
    
    def delete(self, table_name, col):
        command = f"DELETE FROM {table_name} WHERE {col}=?"
        return command
    
    def update(self, table_name, columns):
        cols = ", ".join([f"{col}=?" for col in columns])
        command = f"UPDATE {table_name} SET {cols} WHERE id=?"
        return command

        



