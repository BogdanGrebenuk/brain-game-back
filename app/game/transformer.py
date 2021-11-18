from app.utils.transformer import Transformer


class LeaderboardTransformer(Transformer):

    def __init__(self, player_transformer):
        self._player_transformer = player_transformer

    async def transform(self, leaderboard):
        leaderboard_data = leaderboard.get_leaderboard()
        temp = {}
        for position, player in leaderboard_data.items():
            temp[position] = await self._player_transformer.transform_player_info(player)
        return temp


class PlayerTransformer(Transformer):

    async def transform(self, data):
        return data

    async def transform_session_data(self, player):
        if player.has_any_session():
            data = {
                'session_id': player.get_last_session_id(),
                'session_status': player.get_last_session_status(),
                'session_stage': player.get_last_session_stage(),
                'session_total_score': player.get_last_session_total_score(),
                'session_difficulty': player.get_last_session_difficulty()
            }
        else:
            data = {
                'session_id': None,
                'session_status': None,
                'session_stage': None,
                'session_total_score': None,
                'session_difficulty': None
            }
        return await self.transform(data)

    async def transform_player_info(self, player):
        best_attempt = player.best_attempt
        return {
            'username': player.get_username(),
            'email': player.get_email(),
            'total_score': 0 if best_attempt is None else best_attempt.get_total_score(),
            'passed_all_games': False if best_attempt is None else best_attempt.is_finished(),
            'number': player.get_user_number()
        }
