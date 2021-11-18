from app.game.domain.player import Player
from app.game.domain.session import Session
from app.game.domain.set_of_games import SetOfGames


class PlayerRepository:

    def __init__(self, user_mapper, session_mapper):
        self._user_mapper = user_mapper
        self._session_mapper = session_mapper

    async def get(self, user_id):
        user_structure = await self._user_mapper.get(user_id)
        session_structures = await self._session_mapper.find_by(user_id=user_id)

        player = Player(user_structure, [])
        sessions = []
        for session_structure in session_structures:
            sessions.append(Session(session_structure, player, SetOfGames.default()))

        player._sessions = sessions

        return player

    async def find_all(self):
        users_structures = await self._user_mapper.find_all()
        players = []
        for user_structure in users_structures:
            players.append(await self.get(user_structure.id))
        return players

    # sorry, have no time to implement some kind of UoW
    async def save(self, player):
        await self._user_mapper.update(player._user_structure)
        for session in player._sessions:
            if await self._session_mapper.find(session._session_structure.id):
                await self._session_mapper.update(session._session_structure)
            else:
                await self._session_mapper.create(session._session_structure)
