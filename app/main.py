from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional, List

from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

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




@app.get("/")
def root():
    return {"Hello":"World"}


@app.get("/posts",response_model=List[schemas.ResponsePost]) # We use List because the response is not one dict, but a list of dicts
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    
    new_post = models.Post(
        **post.dict() # Unpacks the dictionary
        )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts/{id}",response_model=schemas.ResponsePost) #Path parameter
def get_post(id:int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.idPost == id).first()
    
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND
            , detail=f"Post with id {id} was not found")
    
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    response = db.query(models.Post).filter(models.Post.idPost == id)

    if not response.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    response.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ResponsePost)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.idPost == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")

    updated_post.update(post.dict(),synchronize_session = False)
    db.commit()

    return updated_post.first()

