from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import  List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.ResponsePost]) # We use List because the response is not one dict, but a list of dicts
def get_posts(db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).all()
    
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **post.dict() # Unpacks the dictionary
        )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    
    return new_post


@router.get("/{id}",response_model=schemas.ResponsePost) #Path parameter
def get_post(id:int, response: Response, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.idPost == id).first()
    
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND
            , detail=f"Post with id {id} was not found")
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    response = db.query(models.Post).filter(models.Post.idPost == id)

    if not response.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    response.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ResponsePost)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.idPost == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")

    updated_post.update(post.dict(),synchronize_session = False)
    db.commit()

    return updated_post.first()