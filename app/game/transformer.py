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
                'sessionId': player.get_last_session_id(),
                'sessionStatus': player.get_last_session_status(),
                'sessionStage': player.get_last_session_stage(),
                'sessionTotalScore': player.get_last_session_total_score(),
                'sessionDifficulty': player.get_last_session_difficulty()
            }
        else:
            data = {
                'sessionId': None,
                'sessionStatus': None,
                'sessionStage': None,
                'sessionTotal_score': None,
                'sessionDifficulty': None
            }
        return await self.transform(data)

    async def transform_player_info(self, player):
        best_attempt = player.best_attempt
        return {
            'username': player.get_username(),
            'email': player.get_email(),
            'totalScore': 0 if best_attempt is None else best_attempt.get_total_score(),
            'passedAllGames': False if best_attempt is None else best_attempt.is_finished(),
            'number': player.get_user_number()
        }
