from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, APIRouter
from .. import schemas, database,models,oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseVote)
def vote(vote: schemas.VoteIn , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.idPost == vote.idPost, models.Vote.idUser == current_user.idUser)
    found_vote = vote_query.first()
    response = schemas.ResponseVote(**vote.dict(), idUser=current_user.idUser)
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.idUser} has already voted on post {vote.idPost}")
        new_vote = models.Vote(idPost = vote.idPost, idUser = current_user.idUser)
        db.add(new_vote)
        db.commit()
        
        return response
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return response