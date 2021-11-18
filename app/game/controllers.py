import uuid

from aiohttp import web

from app.game.domain.leaderboard import Leaderboard
from app.game.domain.set_of_games import SetOfGames


async def get_last_session_info(request, player_repository, player_transformer):
    user_id = request['user_id']

    player = await player_repository.get(user_id)

    return web.json_response(
        await player_transformer.transform_session_data(player),
        status=201
    )


async def start_session(request, player_repository, player_transformer):
    body = await request.json()

    user_id = request['user_id']
    session_difficulty = body['difficulty']
    session_id = str(uuid.uuid4())

    player = await player_repository.get(user_id)

    player.start_new_session(session_id, SetOfGames.default(), session_difficulty)

    await player_repository.save(player)

    return web.json_response(
        await player_transformer.transform_session_data(player),
        status=201
    )


async def complete_stage(request, player_repository, player_transformer):
    user_id = request['user_id']
    body = await request.json()

    player = await player_repository.get(user_id)

    player.move_to_the_next_stage_of_last_session(body['score'])

    await player_repository.save(player)

    return web.json_response(
        await player_transformer.transform_session_data(player),
        status=200
    )


async def close_session_due_to_failure(request, player_repository, player_transformer):
    user_id = request['user_id']

    player = await player_repository.get(user_id)

    player.close_last_session_due_to_failure()

    await player_repository.save(player)

    return web.json_response(
        await player_transformer.transform_session_data(player),
        status=200
    )


async def cancel_session(request, player_repository, player_transformer):
    user_id = request['user_id']

    player = await player_repository.get(user_id)

    player.cancel_last_session()

    await player_repository.save(player)

    return web.json_response(
        await player_transformer.transform_session_data(player),
        status=200
    )


async def get_leaderboard(request, player_repository, leaderboard_transformer):
    players = await player_repository.find_all()

    leaderboard = Leaderboard.from_players(players)

    return web.json_response(
        await leaderboard_transformer.transform(leaderboard),
        status=200
    )


async def compare_images(request, image_comparator):
    body = await request.json()

    original_image = body.get('originalImage')
    drawn_image = body.get('drawnImage')

    distance = await image_comparator.get_distance(original_image, drawn_image)

    return web.json_response(
        {'distance': distance},
        status=200
    )
