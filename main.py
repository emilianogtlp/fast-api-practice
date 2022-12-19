from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"Hello":"World"}

@app.post("/createposts")
def create_posts(post:Post):
    print(post)
    return post