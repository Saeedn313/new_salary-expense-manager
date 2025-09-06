from config import DB_FILE
from .base_db import BaseDb
from models.users import User, Developer, Manager, UserOut



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
                'created_at': 'TEXT DEFAULT CURRENT_TIMESTAMP'
            }
            cursor.execute(self.create_tables(self.table_name, cols))
            self.conn.commit()


    def add_user(self, user_dict: dict):
        user_obj = self.map_role[user_dict["role"]]
        user = user_obj(name= user_dict["name"], family=user_dict["family"])

        cursor = self.conn.cursor()
        columns = ["name", "family", "role"]
        cursor.execute(self.add(self.table_name, columns), (user.name, user.family, user.role))
        user.id = cursor.lastrowid
        self.conn.commit()

        return UserOut(name=user.name, family= user.family, role= user.role, id= user.id)
    
    def get_all_users(self):
        cursor = self.conn.cursor()
        rows = cursor.execute(self.fetch_all(self.table_name)).fetchall()

        all_users = []
        for row in rows:
            user_role = self.map_role[row["role"]]
            user = user_role(name=row["name"], family=row["family"], id=row['user_id'])
            all_users.append(UserOut(name=user.name, family=user.family, role=user.role, id=user.id).dict())

        return all_users

    
    def get_one_user(self, user_id):
        cursor = self.conn.cursor()
        row = cursor.execute(self.fetch_one(self.table_name, "user_id"), (user_id,)).fetchone()

        user_obj = self.map_role[row["role"]]
        user = user_obj(name=row["name"], family=row["family"], id=row["user_id"])

        return UserOut(name=user.name, family=user.family, role=user.role, id=user.id)
    
    def delete_user(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute(self.delete(self.table_name, "user_id"), (user_id, ))
        self.conn.commit()

        # this returns a bool (True, False). 
        # True if the selected row actually effected by execution else False.
        return cursor.rowcount > 0

    def update_user(self, user_id, user_dict: dict):
        user_obj = self.map_role.get(user_dict["role"])
        user = user_obj(name=user_dict["name"], family=user_dict["family"])
        user.id = user_id

        cursor = self.conn.cursor()
        columns = ["name", "family", "role"]
        cursor.execute(self.update(self.table_name, columns, "user_id"), (user.name, user.family, user.role, user.id))
        self.conn.commit()

        return cursor.rowcount > 0