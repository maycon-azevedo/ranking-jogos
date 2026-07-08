from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.scores.model import Score
from app.scores.repository import ScoreRepository
from app.users.repository import UserRepository


class AdminService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.score_repo = ScoreRepository(db)

    def delete_user(self, user_id: int) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuário não encontrado")
        self.user_repo.delete(user)

    def update_score(self, score_id: int, attempts: int) -> Score:
        score = self.score_repo.get_by_id(score_id)
        if not score:
            raise NotFoundError("Score não encontrado")
        return self.score_repo.update(score, attempts)
