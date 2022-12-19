from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

my_posts = [{"title":"First Post", "content":"First Content", "published":True, "id":1},{"title":"Second Post", "content":"Second Content", "published":True,"id":2}]

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
    print(post.dict())
    return post