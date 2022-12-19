from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional

from random import randrange

app = FastAPI()

my_posts = [{"title":"First Post", "content":"First Content", "published":True, "id":1},{"title":"Second Post", "content":"Second Content", "published":True,"id":2}]

def find_post(id):
    for i in my_posts:
        if i['id'] == id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #If the user does not provide a value, de default is True
    rating: Optional[int] = None #Optional field with a default value of none/null


@app.get("/")
def root():
    return {"Hello":"World"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}") #Path parameter
def get_post(id:int):
    post = find_post(id)
    return {"post_detail":post}