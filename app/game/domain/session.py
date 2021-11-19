from dataclasses import dataclass
from datetime import datetime

from app.utils.mapper import Entity


class Session:

    def __init__(self, session_structure, player, set_of_games):
        self._session_structure = session_structure
        self._player = player
        self._set_of_games = set_of_games

    @classmethod
    def new(cls, id_, player, set_of_games, difficulty):
        return cls(
            SessionStructure(
                id=id_,
                user_id=player.get_user_id(),
                status=SessionStatus.IN_PROGRESS,
                total_score=0,
                current_stage=0,
                difficulty=difficulty,
                started_at=datetime.utcnow()
            ),
            player,
            set_of_games
        )

    def move_to_the_next_stage(self, score=0):
        if not self.is_in_progress():
            return

        self._session_structure.total_score += score
        # is on last level
        if self._session_structure.current_stage == (self._set_of_games.get_amount_of_stages() - 1):
            self._session_structure.status = SessionStatus.FINISHED
            return

        self._session_structure.current_stage += 1

    def close_session_due_to_failure(self, score):
        if not self.is_in_progress():
            return
        self._session_structure.total_score += score
        self._session_structure.status = SessionStatus.FAILED

    def cancel_session(self):
        if not self.is_in_progress():
            return
        self._session_structure.status = SessionStatus.CANCELED

    def get_status(self):
        return self._session_structure.status

    def is_in_progress(self):
        return self._session_structure.status == SessionStatus.IN_PROGRESS

    def is_finished(self):
        return self._session_structure.status == SessionStatus.FINISHED

    def is_failed(self):
        return self._session_structure.status == SessionStatus.FAILED

    def is_cancelled(self):
        return self._session_structure.status == SessionStatus.CANCELED

    def get_current_stage(self):
        return self._session_structure.current_stage

    def get_total_score(self):
        return self._session_structure.total_score

    def get_difficulty(self):
        return self._session_structure.difficulty

    def get_id(self):
        return self._session_structure.id

    def get_started_at(self):
        return self._session_structure.started_at


@dataclass
class SessionStructure(Entity):
    id: str
    user_id: str
    status: int
    total_score: int
    current_stage: int
    difficulty: int
    started_at: datetime


class SessionStatus:
    IN_PROGRESS = 0
    FINISHED = 1
    FAILED = 2
    CANCELED = 3
