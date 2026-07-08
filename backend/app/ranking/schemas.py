from datetime import date as DateType
from enum import Enum

from pydantic import BaseModel

from app.enums import GameName


class RankingPeriod(str, Enum):
    HOJE = "hoje"
    SEMANA = "semana"
    MES = "mes"
    TODOS = "todos"


class RankingEntry(BaseModel):
    position: int
    user_id: int
    username: str
    avatar_url: str | None = None
    game_victories: int
    daily_championships: int
    avg_attempts: float
    total_games: int
    streak: int
    win_streak: int = 0


class GameRankingEntry(BaseModel):
    position: int
    user_id: int
    username: str
    avatar_url: str | None = None
    victories: int
    avg_attempts: float
    total_games: int


class DailyChampionResponse(BaseModel):
    user_id: int
    username: str
    avatar_url: str | None = None
    victories: int
    total_attempts: int
    is_provisional: bool


class TodayHighlight(BaseModel):
    game: GameName
    user_id: int | None = None
    username: str | None = None
    avatar_url: str | None = None
    attempts: int | None = None


class AttemptsDistribution(BaseModel):
    attempts: int
    count: int


class CalendarDay(BaseModel):
    date: DateType
    games_played: int


class RecordEntry(BaseModel):
    title: str
    description: str
    icon: str
    user_id: int
    username: str
    avatar_url: str | None = None
    value: str
    game: GameName | None = None


class RecordsResponse(BaseModel):
    records: list[RecordEntry]


class CompareGameResult(BaseModel):
    game: GameName
    avg_p1: float
    avg_p2: float
    victories_p1: int
    victories_p2: int


class CompareResponse(BaseModel):
    player1_id: int
    player1_username: str
    player2_id: int
    player2_username: str
    games: list[CompareGameResult]
