from config import DB_FILE
from .base_db import BaseDb
from models.db_models.users import Developer, Manager
from datetime import datetime



class UserDb(BaseDb):
    def __init__(self):
        super().__init__()
        self.table_name = "users"
        self.map_role = {"Manager": Manager, "Developer": Developer}

    def create_user_tables(self):
            cursor = self.conn.cursor()
            cols = {
                'user_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'name': 'TEXT NOT NULL',
                'family': 'TEXT NOT NULL',
                'role': 'TEXT NOT NULL',
                'created_at': 'TEXT'
            }
            cursor.execute(self.create_tables(self.table_name, cols))
            self.conn.commit()


    def add_user(self, user_dict: dict):
        user_obj = self.map_role[user_dict["role"]]
        time_stamp = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        user = user_obj(name= user_dict["name"], family=user_dict["family"], created_at=time_stamp)

        cursor = self.conn.cursor()
        columns = ["name", "family", "role", "created_at"]
        cursor.execute(self.add(self.table_name, columns), (user.name, user.family, user.role, user.created_at))
        user.id = cursor.lastrowid
        self.conn.commit()
        
        return user
    
    def get_all_users(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()

        all_users = []
        for row in rows:
            user_role = self.map_role[row["role"]]
            user = user_role(name=row["name"], family=row["family"], id=row['user_id'], created_at=row["created_at"])
            all_users.append(user)

        return all_users

    
    def get_one_user(self, user_id):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "user_id"), (user_id,)).fetchone()

        user_obj = self.map_role[row["role"]]
        user = user_obj(name=row["name"], family=row["family"], id=row["user_id"], created_at=row["created_at"])

        return user if user is not None else None
    
    def delete_user(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "user_id"), (user_id, ))
        self.conn.commit()

        # this returns a bool (True, False). 
        # True if the selected row actually effected by execution else False.
        return cursor.rowcount > 0

    def update_user(self, user_id, user_dict: dict):
        user_obj = self.map_role.get(user_dict["role"])
        user = user_obj(name=user_dict["name"], family=user_dict["family"], id=user_id)

        cursor = self.conn.cursor()
        columns = ["name", "family", "role"]
        cursor.execute(self.update(self.table_name, columns, "user_id"), (user.name, user.family, user.role, user.id))
        self.conn.commit()

        return cursor.rowcount > 0