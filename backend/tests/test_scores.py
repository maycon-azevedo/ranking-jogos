"""Tests for score submission rules."""

from datetime import date
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.scores.model import Score
from app.scores.service import ScoreService
from app.users.model import User


class FakeRepo:
    def __init__(self):
        self.scores: list[Score] = []
        self._id = 0

    def get_by_user_game_date(self, user_id, game, played_date):
        for s in self.scores:
            if s.user_id == user_id and s.game == game.value and s.played_date == played_date:
                return s
        return None

    def get_by_id(self, score_id):
        for s in self.scores:
            if s.id == score_id:
                return s
        return None

    def create(self, user_id, game, played_date, attempts):
        self._id += 1
        s = Score.__new__(Score)
        s.id = self._id
        s.user_id = user_id
        s.game = game.value
        s.played_date = played_date
        s.attempts = attempts
        self.scores.append(s)
        return s

    def update(self, score, attempts):
        score.attempts = attempts
        return score

    def delete(self, score):
        self.scores.remove(score)


def make_user(uid=1, is_admin=False):
    u = User.__new__(User)
    u.id = uid
    u.username = "testuser"
    u.is_admin = is_admin
    return u


TODAY = date(2025, 6, 14)


class TestScoreSubmission:
    def _make_service(self):
        svc = ScoreService.__new__(ScoreService)
        svc.repo = FakeRepo()
        return svc

    @patch("app.scores.service.today_manaus", return_value=TODAY)
    def test_submit_creates_new_score(self, mock_today):
        from app.scores.schemas import ScoreCreate
        from app.enums import GameName

        svc = self._make_service()
        user = make_user()
        score = svc.submit_score(user, ScoreCreate(game=GameName.CONEXO, attempts=3))
        assert score.attempts == 3
        assert score.game == "conexo"
        assert score.played_date == TODAY

    @patch("app.scores.service.today_manaus", return_value=TODAY)
    def test_submit_upserts_existing(self, mock_today):
        from app.scores.schemas import ScoreCreate
        from app.enums import GameName

        svc = self._make_service()
        user = make_user()
        s1 = svc.submit_score(user, ScoreCreate(game=GameName.CONEXO, attempts=3))
        s2 = svc.submit_score(user, ScoreCreate(game=GameName.CONEXO, attempts=2))
        assert s1.id == s2.id
        assert s2.attempts == 2

    @patch("app.scores.service.today_manaus", return_value=TODAY)
    def test_edit_blocked_for_past_score(self, mock_today):
        svc = self._make_service()
        user = make_user()

        past_score = Score.__new__(Score)
        past_score.id = 99
        past_score.user_id = user.id
        past_score.played_date = date(2025, 6, 10)
        past_score.attempts = 3
        svc.repo.scores.append(past_score)

        with pytest.raises(HTTPException) as exc_info:
            svc.update_score(user, 99, 2)
        assert exc_info.value.status_code == 403

    @patch("app.scores.service.today_manaus", return_value=TODAY)
    def test_admin_can_edit_past_score(self, mock_today):
        svc = self._make_service()
        admin = make_user(uid=1, is_admin=True)

        past_score = Score.__new__(Score)
        past_score.id = 99
        past_score.user_id = admin.id
        past_score.played_date = date(2025, 6, 10)
        past_score.attempts = 3
        svc.repo.scores.append(past_score)

        result = svc.update_score(admin, 99, 1)
        assert result.attempts == 1

    @patch("app.scores.service.today_manaus", return_value=TODAY)
    def test_cannot_edit_other_user_score(self, mock_today):
        svc = self._make_service()
        user1 = make_user(uid=1)
        user2 = make_user(uid=2)

        score = Score.__new__(Score)
        score.id = 50
        score.user_id = user1.id
        score.played_date = TODAY
        score.attempts = 3
        svc.repo.scores.append(score)

        with pytest.raises(HTTPException) as exc_info:
            svc.update_score(user2, 50, 1)
        assert exc_info.value.status_code == 403
