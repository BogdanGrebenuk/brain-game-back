from aiohttp import web


async def get_user_me(request, user_transformer):
    user = request['user']

    return web.json_response(await user_transformer.transform(user))
