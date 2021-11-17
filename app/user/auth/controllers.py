import uuid

from aiohttp import web

from app.user.auth.dto import CreateUserDto, AuthenticateUserDto


async def authenticate_user(request, authenticator):
    body = await request.json()

    token = await authenticator.authenticate(
        AuthenticateUserDto(
            email=body.get('email'),
            password=body.get('password')
        )
    )

    return web.json_response({'token': token})


async def register_user(
        request,
        registrar,
        user_mapper,
        user_transformer
        ):
    body = await request.json()

    user = await registrar.register(
        CreateUserDto(
            id=str(uuid.uuid4()),
            email=body.get('email'),
            password=body.get('password'),
            first_name=body.get('first_name'),
            last_name=body.get('last_name'),
            patronymic=body.get('patronymic'),
            role=body.get('role')
        )
    )

    await user_mapper.create(user)

    return web.json_response(await user_transformer.transform(user))


async def logout_user(request, user_mapper):
    user = await user_mapper.find(request.get('user_id'))

    user.token = None

    await user_mapper.update(user)

    return web.json_response({})
