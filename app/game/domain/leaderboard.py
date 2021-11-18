class Leaderboard:

    def __init__(self, players):
        self._players = players

    @classmethod
    def from_players(cls, players):
        return cls(players)

    def get_leaderboard(self):
        players_with_finished_sessions = filter(
            lambda player: player.has_any_finished_or_failed_session(),
            self._players
        )
        sorted_players = sorted(
            players_with_finished_sessions,
            key=self._player_comparator,
            reverse=True
        )
        temp = {}
        for position, player in enumerate(sorted_players):
            temp[position+1] = player
        return temp

    def _player_comparator(self, player):
        best_attempt = player.best_attempt
        if best_attempt is None:
            return 0, 0
        return self._normalize_attempt_status(best_attempt), best_attempt.get_total_score()

    def _normalize_attempt_status(self, session):
        if session.is_finished():
            return 1
        return 0
