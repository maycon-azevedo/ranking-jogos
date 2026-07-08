"""Tests for victory computation logic."""

from collections import defaultdict
from datetime import date

import pytest

from app.ranking.service import RankingService


class FakeScore:
    def __init__(self, user_id: int, game: str, played_date: date, attempts: int):
        self.user_id = user_id
        self.game = game
        self.played_date = played_date
        self.attempts = attempts


DAY = date(2025, 6, 1)


class TestVictoryComputation:
    def _compute(self, scores):
        svc = object.__new__(RankingService)
        return svc._compute_victories(scores)

    def test_single_winner(self):
        scores = [
            FakeScore(1, "conexo", DAY, 2),
            FakeScore(2, "conexo", DAY, 4),
            FakeScore(3, "conexo", DAY, 5),
        ]
        victories, _ = self._compute(scores)
        assert victories[(1, DAY)] == 1
        assert victories.get((2, DAY), 0) == 0
        assert victories.get((3, DAY), 0) == 0

    def test_shared_victory_on_tie(self):
        scores = [
            FakeScore(1, "conexo", DAY, 2),
            FakeScore(2, "conexo", DAY, 2),
            FakeScore(3, "conexo", DAY, 5),
        ]
        victories, _ = self._compute(scores)
        assert victories[(1, DAY)] == 1
        assert victories[(2, DAY)] == 1
        assert victories.get((3, DAY), 0) == 0

    def test_multiple_games_accumulate(self):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(2, "conexo", DAY, 3),
            FakeScore(1, "letroso", DAY, 1),
            FakeScore(2, "letroso", DAY, 1),
            FakeScore(1, "expresso", DAY, 5),
            FakeScore(2, "expresso", DAY, 2),
        ]
        victories, attempts = self._compute(scores)
        assert victories[(1, DAY)] == 2  # conexo + letroso
        assert victories[(2, DAY)] == 2  # letroso + expresso
        assert attempts[(1, DAY)] == 7   # 1+1+5
        assert attempts[(2, DAY)] == 6   # 3+1+2


class TestChampionComputation:
    def _compute_champions(self, scores):
        svc = object.__new__(RankingService)
        return svc._compute_champions(scores)

    def test_champion_requires_triad(self):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(1, "letroso", DAY, 1),
            # user 1 missing expresso — no triad
            FakeScore(2, "conexo", DAY, 5),
            FakeScore(2, "letroso", DAY, 5),
            FakeScore(2, "expresso", DAY, 5),
        ]
        champions = self._compute_champions(scores)
        assert champions.get(DAY) == [2]

    def test_champion_most_victories(self):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(1, "letroso", DAY, 1),
            FakeScore(1, "expresso", DAY, 1),
            FakeScore(2, "conexo", DAY, 3),
            FakeScore(2, "letroso", DAY, 3),
            FakeScore(2, "expresso", DAY, 3),
        ]
        champions = self._compute_champions(scores)
        # user 1 wins all 3 games
        assert champions[DAY] == [1]

    def test_champion_tiebreak_by_attempts(self):
        scores = [
            FakeScore(1, "conexo", DAY, 2),
            FakeScore(1, "letroso", DAY, 2),
            FakeScore(1, "expresso", DAY, 2),  # total: 6
            FakeScore(2, "conexo", DAY, 2),
            FakeScore(2, "letroso", DAY, 2),
            FakeScore(2, "expresso", DAY, 1),  # total: 5
        ]
        champions = self._compute_champions(scores)
        # both tie on victories (3 shared), user 2 lower total
        assert champions[DAY] == [2]

    def test_champion_shared_on_full_tie(self):
        scores = [
            FakeScore(1, "conexo", DAY, 2),
            FakeScore(1, "letroso", DAY, 2),
            FakeScore(1, "expresso", DAY, 2),
            FakeScore(2, "conexo", DAY, 2),
            FakeScore(2, "letroso", DAY, 2),
            FakeScore(2, "expresso", DAY, 2),
        ]
        champions = self._compute_champions(scores)
        assert sorted(champions[DAY]) == [1, 2]

    def test_no_champion_without_triad(self):
        scores = [
            FakeScore(1, "conexo", DAY, 1),
            FakeScore(1, "letroso", DAY, 1),
            FakeScore(2, "conexo", DAY, 3),
            FakeScore(2, "letroso", DAY, 3),
        ]
        champions = self._compute_champions(scores)
        assert DAY not in champions
