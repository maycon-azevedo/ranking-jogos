from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.enums import GameName
from app.ranking.schemas import (
    AttemptsDistribution,
    CalendarDay,
    CompareResponse,
    DailyChampionResponse,
    GameRankingEntry,
    RankingEntry,
    RankingPeriod,
    RecordsResponse,
)
from app.ranking.service import RankingService
from app.users.model import User

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/general", response_model=list[RankingEntry])
def get_general_ranking(
    period: RankingPeriod = Query(RankingPeriod.TODOS),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_general_ranking(period)


@router.get("/game/{game}", response_model=list[GameRankingEntry])
def get_game_ranking(
    game: GameName,
    period: RankingPeriod = Query(RankingPeriod.TODOS),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_game_ranking(game, period)


@router.get("/champion/today", response_model=list[DailyChampionResponse])
def get_today_champion(
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_today_champion()


@router.get("/stats/distribution", response_model=list[AttemptsDistribution])
def get_distribution(
    user_id: int | None = Query(None),
    game: GameName | None = Query(None),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_distribution(user_id=user_id, game=game)


@router.get("/stats/calendar", response_model=list[CalendarDay])
def get_calendar(
    user_id: int = Query(...),
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_calendar(user_id)


@router.get("/records", response_model=RecordsResponse)
def get_records(
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).get_records()


@router.get("/compare/{p1_id}/{p2_id}", response_model=CompareResponse)
def compare_players(
    p1_id: int,
    p2_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RankingService(db).compare_players(p1_id, p2_id)
