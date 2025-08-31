# from models.users import Developer, Manager, User
# from db.user_db import UserDb
# from fastapi import FastAPI
# import json

# app = FastAPI()
# user_db = UserDb()

# @app.get('/')
# def home():
#     # dev1 = Developer('hassan', 'nazari', 300, 15, 53)
#     # all_users = dev1.get_all_users()
#     # dev1.delete_user(len(all_users))
#     # users = {}
#     # for ind, user in enumerate(all_users):
#     #     users[ind] = to_dict(user)
    
#     # return users
#     pass

# @app.post('/users/{user_id}')
# def create_user(user_id):
    



    
# def to_dict(user):
#     return {
#         'name': user.name,
#         'family': user.family,
#         'fullname': user.full_name()
#     }


# from fastapi import FastAPI, HTTPException, status
# from fastapi.params import Body
# from pydantic import BaseModel
# from typing import Optional

# app = FastAPI()

# my_posts =[{
#             "title": "First Post",
#             "content": "This is the first content.",
#             "publish": True,
#             "rating": 5,
#             "id": 1
#         },{
#             "title": "Second Post",
#             "content": "This is the second content.",
#             "publish": False,
#             "rating": 3,
#             "id": 2
#         }]


# def find_by_id(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post
        
# def find_ind_post(id):
#     for ind , post in enumerate(my_posts):
#         if post['id'] == id:
#             return ind



# class Post(BaseModel):
    
#     title: str
#     content: str
#     poblished: bool = True
#     rating: Optional[int] = None
#     id: int

# @app.get("/")
# def root():
#     return {'massage': "Hello World!"}

# @app.get("/post")
# def posts():
#     return {"data": my_posts}


# @app.post('/posts')
# def create_user(post: Post):
#     my_posts.append(post.dict())
#     return {'new post': post.dict(), 'allposts': my_posts}

# @app.get('/posts/{id}')
# def get_post(id: int):
#     post = find_by_id(id)
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found!")
    
#     return {"post": post}

# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     ind = find_ind_post(id)
#     if ind == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {id} does not exist!')
#     my_posts.pop(ind)
#     print(my_posts)
#     return {'message': 'Post is deleted successfully'}

# @app.put('/posts/{id}')
# def update_post(id: int, post:Post):
#     ind = find_ind_post(id)
#     if ind == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post with id: {id} not found!')
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[ind] = post_dict
#     return {"data": post_dict}


# from models.users import User, Developer, Manager
# from db.user_db import UserDb
# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel

# app = FastAPI()
# user_db = UserDb()
# user_db.init_db()

# class UserIn(BaseModel):
#     name: str
#     family: str
#     role: str
#     hourly_rate: int
#     total_hour: int
#     total_minute: int


# class UserOut(UserIn):
#     id: int
#     salary: int

# @app.get("/")
# def home():
#     return {"response": "welcome"}

# @app.get('/users')
# def get_users():
#     users = []
#     rows = user_db.fetch_all()
#     for row in rows:
#         user_id, name, family, role, hourly_rate, total_hour, total_minute = row
#         if role == "Developer":
#             user = Developer(name, family, hourly_rate, total_hour, total_minute)
#         elif role == "Manager":
#             user = Manager(name, family, hourly_rate, total_hour, total_minute)
#         user.id = user_id
#         user.salary = user.calc_salary()

#         users.append(user)

#     return {"users": users}


# @app.get("/users/{id}")
# def get_user(id):
#     row = user_db.fetch_one(id)
#     if row is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found")
#     user_id, name, family, role, hourly_rate, total_hour, total_minute = row
#     if role == "Developer":
#         user = Developer(name, family, hourly_rate, total_hour, total_minute)
#     elif role == "Manager":
#         user = Manager(name, family, hourly_rate, total_hour, total_minute)

#     user.id = user_id
#     user.salary = user.calc_salary()
#     return {"user": user}

# @app.post("/users")
# def create_user(user: UserIn):
#     # new_user = user_db.add(user.dict())
#     user_dict = user.dict()
#     if user_dict['role'] == "Developer":
#         user = Developer(user_dict['name'], user_dict['family'], user_dict['hourly_rate'], user_dict['total_hour'], user_dict['total_minute'])
#     elif user_dict['role'] == "Manager":
#         user = Manager(user_dict['name'], user_dict['family'], user_dict['hourly_rate'], user_dict['total_hour'], user_dict['total_minute'])

#     new_user = user_db.add(user)
#     return {"new user": new_user}

# @app.delete("/users/{id}")
# def delete_user(id):
#     user = user_db.fetch_one(id)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
#     user_db.delete(id)
#     return {"detail": "user deleted!"}

# @app.put("/users/{id}")
# def updata_user(id, user_in: UserIn):
#     user_dict = user_in.dict()
#     if user_dict['role'] == "Developer":
#         updated_user = Developer(user_dict['name'], user_dict['family'], user_dict['hourly_rate'], user_dict['total_hour'], user_dict['total_minute'])
#     elif user_dict['role'] == "Manager":
#         updated_user = Manager(user_dict['name'], user_dict['family'], user_dict['hourly_rate'], user_dict['total_hour'], user_dict['total_minute'])
    
#     updated_user.id = id
#     user_db.update(updated_user)
#     return {"detail": f"user updated {updated_user}"}



# print(user_in.dict)
# user_exist = user_db.fetch_one(id)
# if user_exist is None:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found!")

from fastapi import FastAPI
from api.routers import user, cost

app = FastAPI()
app.include_router(user.router)
app.include_router(cost.router)

@app.get("/")
def home():
    return "welcome to fastapi"

