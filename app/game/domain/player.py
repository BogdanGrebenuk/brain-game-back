from app.exceptions.application import DomainException
from app.game.domain.session import Session


class Player:

    def __init__(self, user_structure, sessions):
        self._user_structure = user_structure
        self._sessions = sessions

    @property
    def last_session(self):
        if len(self._sessions) == 0:
            raise DomainException('Player has no any session')
        return max(self._sessions, key=lambda session: session.get_started_at().timestamp())

    def has_any_session(self):
        try:
            last_session = self.last_session
            return True
        except DomainException:
            return False

    def has_any_finished_or_failed_session(self):
        for session in self._sessions:
            if session.is_finished() or session.is_failed():
                return True
        return False

    def start_new_session(self, session_id, set_of_games, difficulty):
        self._cancel_sessions_with_in_progress_status()
        session = Session.new(session_id, self, set_of_games, difficulty)
        self._sessions.append(session)

    @property
    def best_attempt(self):
        finished_sessions = [
            session
            for session in self._sessions
            if session.is_finished() or session.is_failed()
        ]
        if len(finished_sessions) == 0:
            return None
        return max(finished_sessions, key=lambda session: session.get_total_score())

    def move_to_the_next_stage_of_last_session(self, score=0):
        self.last_session.move_to_the_next_stage(score)

    def close_last_session_due_to_failure(self):
        self.last_session.close_session_due_to_failure()

    def cancel_last_session(self):
        self.last_session.cancel_session()

    def _cancel_sessions_with_in_progress_status(self):
        for session in self._sessions:
            if not session.is_in_progress():
                continue
            session.cancel_session()

    def get_user_id(self):
        return self._user_structure.id

    def get_username(self):
        return self._user_structure.username

    def get_user_number(self):
        return self._user_structure.number

    def get_email(self):
        return self._user_structure.email

    def get_last_session_status(self):
        return self.last_session.get_status()

    def get_last_session_stage(self):
        return self.last_session.get_current_stage()

    def get_last_session_total_score(self):
        return self.last_session.get_total_score()

    def get_last_session_difficulty(self):
        return self.last_session.get_difficulty()

    def get_last_session_id(self):
        return self.last_session.get_id()