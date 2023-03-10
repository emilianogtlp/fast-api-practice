from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from .. import models,schemas,oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import  List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.ResponsePostVote]) # We use List because the response is not one dict, but a list of dicts
def get_posts(
    db: Session = Depends(get_db),
    user_id:int = Depends(oauth2.get_current_user),
    limit:int = 10,
    skip:int = 0,
    search: Optional[str] = ""):

    posts = db.query(models.Post,func.count(
        models.Vote.idPost).label("Votes")).join(
            models.Vote, models.Post.idPost == models.Vote.idPost, isouter=True
            ).group_by(models.Post.idPost).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponsePost)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    #print(current_user.idUser)
    new_post = models.Post(
        idUser = current_user.idUser, **post.dict() # Unpacks the dictionary
        )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}",response_model=schemas.ResponsePostVote) #Path parameter
def get_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(
        models.Post, func.count(models.Vote.idPost).label("Votes")
        ).join(
            models.Vote, models.Post.idPost == models.Vote.idPost, isouter=True
            ).group_by(
                models.Post.idPost
            ).filter(models.Post.idPost == id).first()
    
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND
            , detail=f"Post with id {id} was not found")
    
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    response_query = db.query(models.Post).filter(models.Post.idPost == id)
    response = response_query.first()

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    if response.idUser != current_user.idUser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    response_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ResponsePost)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    updated_post_query = db.query(models.Post).filter(models.Post.idPost == id)
    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} does not exist")
    
    if updated_post.idUser != current_user.idUser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    updated_post_query.update(post.dict(),synchronize_session = False)
    db.commit()

    return updated_post