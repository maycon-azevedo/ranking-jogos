from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.enums import GameName


class _AttemptsValidator(BaseModel):
    attempts: int

    @field_validator("attempts")
    @classmethod
    def attempts_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("attempts deve ser >= 1")
        return v


class ScoreCreate(_AttemptsValidator):
    game: GameName


class ScoreUpdate(_AttemptsValidator):
    pass


class ScoreBatchCreate(BaseModel):
    scores: list[ScoreCreate]


class ScoreResponse(BaseModel):
    id: int
    user_id: int
    game: GameName
    played_date: date
    attempts: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
