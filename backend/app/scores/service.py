from sqlalchemy.orm import Session

from app.config import today_manaus
from app.exceptions import ForbiddenError, NotFoundError
from app.scores.model import Score
from app.scores.repository import ScoreRepository
from app.scores.schemas import ScoreCreate
from app.users.model import User


class ScoreService:
    def __init__(self, db: Session):
        self.repo = ScoreRepository(db)

    def submit_score(self, user: User, data: ScoreCreate) -> Score:
        today = today_manaus()
        existing = self.repo.get_by_user_game_date(user.id, data.game, today)
        if existing:
            return self.repo.update(existing, data.attempts)
        return self.repo.create(user.id, data.game, today, data.attempts)

    def submit_batch(self, user: User, scores: list[ScoreCreate]) -> list[Score]:
        return [self.submit_score(user, s) for s in scores]

    def get_today_scores(self, user: User) -> list[Score]:
        return self.repo.get_user_today_scores(user.id, today_manaus())

    def update_score(self, user: User, score_id: int, attempts: int) -> Score:
        score = self._get_owned_score(user, score_id)
        return self.repo.update(score, attempts)

    def delete_score(self, user: User, score_id: int) -> None:
        score = self._get_owned_score(user, score_id)
        self.repo.delete(score)

    def _get_owned_score(self, user: User, score_id: int) -> Score:
        score = self.repo.get_by_id(score_id)
        if not score:
            raise NotFoundError("Score não encontrado")
        if score.user_id != user.id and not user.is_admin:
            raise ForbiddenError("Sem permissão")
        if score.played_date != today_manaus() and not user.is_admin:
            raise ForbiddenError("Só é possível alterar scores do dia atual")
        return score
