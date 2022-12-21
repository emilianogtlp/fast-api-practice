from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional

from random import randrange
import time

import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password123',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful.")
        break
    except Exception as error:
        print(error)
        print("Connection to database failed")
        time.sleep(3)

my_posts = [{"title":"First Post", "content":"First Content", "published":True, "id":1},{"title":"Second Post", "content":"Second Content", "published":True,"id":2}]

def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #If the user does not provide a value, de default is True
    #rating: Optional[int] = None #Optional field with a default value of none/null


@app.get("/")
def root():
    return {"Hello":"World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post """)
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(
        """INSERT INTO post (title, content, published) VALUES (%s,%s,%s) RETURNING *;""",
        (post.title,post.content,post.published)
    )
    new_post = cursor.fetchone()
    conn.commit() #Commit the changes
    return {"data":new_post}

@app.get("/posts/{id}") #Path parameter
def get_post(id:int, response: Response):
    cursor.execute(
        """SELECT * FROM post WHERE id = %s;""",
        (str(id))
    )
    post = cursor.fetchone()
    print(post)
    #conn.commit()
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND
            , detail=f"Post with id {id} was not found")
    
    return {"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id:int, post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'data':post_dict}