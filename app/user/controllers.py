from aiohttp import web


async def get_user(request, user_mapper, user_transformer):
    user_id = request.match_info.get('user_id')
    if user_id == 'me':
        user_id = request['user_id']

    user = await user_mapper.find(user_id)
    if user is None:
        return web.json_response({
            'error': 'User not found',
            'payload': {'user_id': user_id}
        }, status=404)

    return web.json_response({
        'user': await user_transformer.transform(user)
    })


async def get_users(request, user_mapper, user_transformer):
    users = await user_mapper.find_all()

    return web.json_response({
        'users': await user_transformer.transform_many(users)
    })
