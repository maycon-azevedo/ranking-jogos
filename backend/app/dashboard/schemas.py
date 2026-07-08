from pydantic import BaseModel

from app.enums import GameName
from app.ranking.schemas import DailyChampionResponse, TodayHighlight


class TriadStatus(BaseModel):
    game: GameName
    played: bool
    attempts: int | None = None
    score_id: int | None = None


class FriendActivity(BaseModel):
    user_id: int
    username: str
    avatar_url: str | None = None
    games_played: int
    games: list[GameName]


class DashboardResponse(BaseModel):
    triad: list[TriadStatus]
    streak: int
    highlights: list[TodayHighlight]
    champions: list[DailyChampionResponse]
    friends_activity: list[FriendActivity]
