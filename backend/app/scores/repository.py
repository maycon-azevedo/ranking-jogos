from collections import defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.enums import GameName
from app.scores.model import Score


class ScoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, score_id: int) -> Score | None:
        return self.db.query(Score).filter(Score.id == score_id).first()

    def get_by_user_game_date(
        self, user_id: int, game: GameName, played_date: date,
    ) -> Score | None:
        return self.db.query(Score).filter(
            Score.user_id == user_id,
            Score.game == game.value,
            Score.played_date == played_date,
        ).first()

    def get_user_today_scores(self, user_id: int, today: date) -> list[Score]:
        return self.db.query(Score).filter(
            Score.user_id == user_id,
            Score.played_date == today,
        ).all()

    def get_scores_in_period(
        self,
        start_date: date,
        end_date: date,
        game: GameName | None = None,
    ) -> list[Score]:
        query = self.db.query(Score).filter(
            Score.played_date >= start_date,
            Score.played_date <= end_date,
        )
        if game:
            query = query.filter(Score.game == game.value)
        return query.all()

    def get_all_scores(self, game: GameName | None = None) -> list[Score]:
        query = self.db.query(Score)
        if game:
            query = query.filter(Score.game == game.value)
        return query.all()

    def get_user_all_scores(self, user_id: int) -> list[Score]:
        return (
            self.db.query(Score)
            .filter(Score.user_id == user_id)
            .order_by(Score.played_date.desc())
            .all()
        )

    def get_user_played_dates(self, user_id: int) -> set[date]:
        rows = (
            self.db.query(Score.played_date)
            .filter(Score.user_id == user_id)
            .distinct()
            .all()
        )
        return {r[0] for r in rows}

    def get_all_played_dates(self) -> dict[int, set[date]]:
        rows = (
            self.db.query(Score.user_id, Score.played_date)
            .distinct()
            .all()
        )
        result: dict[int, set[date]] = defaultdict(set)
        for uid, d in rows:
            result[uid].add(d)
        return result

    def create(
        self, user_id: int, game: GameName, played_date: date, attempts: int,
    ) -> Score:
        score = Score(
            user_id=user_id,
            game=game.value,
            played_date=played_date,
            attempts=attempts,
        )
        self.db.add(score)
        self.db.commit()
        self.db.refresh(score)
        return score

    def update(self, score: Score, attempts: int) -> Score:
        score.attempts = attempts
        self.db.commit()
        self.db.refresh(score)
        return score

    def delete(self, score: Score) -> None:
        self.db.delete(score)
        self.db.commit()
