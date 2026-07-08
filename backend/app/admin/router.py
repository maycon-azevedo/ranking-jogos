from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.admin.service import AdminService
from app.auth.dependencies import get_admin_user
from app.database import get_db
from app.scores.schemas import ScoreResponse, ScoreUpdate
from app.users.model import User
from app.users.schemas import UserResponse
from app.users.repository import UserRepository

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    _admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return UserRepository(db).get_all()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    _admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    AdminService(db).delete_user(user_id)


@router.put("/scores/{score_id}", response_model=ScoreResponse)
def update_score(
    score_id: int,
    body: ScoreUpdate,
    _admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return AdminService(db).update_score(score_id, body.attempts)
