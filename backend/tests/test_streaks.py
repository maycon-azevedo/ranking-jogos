"""Tests for streak calculations."""

from collections import defaultdict
from datetime import date, timedelta
from unittest.mock import patch

from app.ranking.service import RankingService


DAY = date(2025, 6, 14)


class FakeScoreRepo:
    def __init__(self, played_dates=None, scores=None):
        self._played_dates = played_dates or set()
        self._scores = scores or []

    def get_user_played_dates(self, user_id):
        return self._played_dates

    def get_all_scores(self):
        return self._scores


class FakeScore:
    def __init__(self, user_id, game, played_date, attempts):
        self.user_id = user_id
        self.game = game
        self.played_date = played_date
        self.attempts = attempts


class TestPlayStreak:
    def _make_service(self, played_dates):
        svc = RankingService.__new__(RankingService)
        svc.score_repo = FakeScoreRepo(played_dates=played_dates)
        return svc

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_streak_consecutive_days(self, _):
        dates = {DAY, DAY - timedelta(days=1), DAY - timedelta(days=2)}
        svc = self._make_service(dates)
        assert svc._calculate_streak(1) == 3

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_streak_broken_gap(self, _):
        dates = {DAY, DAY - timedelta(days=1), DAY - timedelta(days=3)}
        svc = self._make_service(dates)
        assert svc._calculate_streak(1) == 2

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_streak_zero_no_today(self, _):
        dates = {DAY - timedelta(days=1), DAY - timedelta(days=2)}
        svc = self._make_service(dates)
        assert svc._calculate_streak(1) == 0

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_streak_empty(self, _):
        svc = self._make_service(set())
        assert svc._calculate_streak(1) == 0


class TestWinStreak:
    def _make_service(self, scores):
        svc = RankingService.__new__(RankingService)
        svc.score_repo = FakeScoreRepo(scores=scores)
        return svc

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_win_streak_consecutive(self, _):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(2, "conexo", DAY, 3),
            FakeScore(1, "conexo", DAY - timedelta(days=1), 1),
            FakeScore(2, "conexo", DAY - timedelta(days=1), 3),
            FakeScore(1, "conexo", DAY - timedelta(days=2), 1),
            FakeScore(2, "conexo", DAY - timedelta(days=2), 3),
        ]
        svc = self._make_service(scores)
        assert svc._calculate_win_streak(1) == 3

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_win_streak_breaks_on_loss(self, _):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(2, "conexo", DAY, 3),
            FakeScore(1, "conexo", DAY - timedelta(days=1), 5),
            FakeScore(2, "conexo", DAY - timedelta(days=1), 1),  # user 2 wins
            FakeScore(1, "conexo", DAY - timedelta(days=2), 1),
            FakeScore(2, "conexo", DAY - timedelta(days=2), 3),
        ]
        svc = self._make_service(scores)
        # user 1: won today, lost yesterday → streak = 1
        assert svc._calculate_win_streak(1) == 1

    @patch("app.ranking.service.today_manaus", return_value=DAY)
    def test_win_streak_zero_no_win_today(self, _):
        scores = [
            FakeScore(1, "conexo", DAY, 5),
            FakeScore(2, "conexo", DAY, 1),
        ]
        svc = self._make_service(scores)
        assert svc._calculate_win_streak(1) == 0
