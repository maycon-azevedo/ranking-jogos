from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.scores.repository import ScoreRepository
from app.scores.schemas import ScoreBatchCreate, ScoreResponse, ScoreUpdate
from app.scores.service import ScoreService
from app.users.model import User

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/mine", response_model=list[ScoreResponse])
def get_my_scores(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ScoreRepository(db).get_user_all_scores(user.id)


@router.get("/today", response_model=list[ScoreResponse])
def get_today_scores(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ScoreService(db).get_today_scores(user)


@router.post("", response_model=list[ScoreResponse], status_code=status.HTTP_201_CREATED)
def submit_scores(
    body: ScoreBatchCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ScoreService(db).submit_batch(user, body.scores)


@router.put("/{score_id}", response_model=ScoreResponse)
def update_score(
    score_id: int,
    body: ScoreUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ScoreService(db).update_score(user, score_id, body.attempts)


@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_score(
    score_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ScoreService(db).delete_score(user, score_id)
