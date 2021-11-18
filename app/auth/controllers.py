import uuid

from aiohttp import web

from app.auth.dto import AuthenticateUserDto, CreateUserDto


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
        auth_user_transformer,
        user_number_generator
        ):
    body = await request.json()

    user_number = await user_number_generator.generate()

    user = await registrar.register(
        CreateUserDto(
            id=str(uuid.uuid4()),
            email=body.get('email'),
            password=body.get('password'),
            username=body.get('username'),
            number=user_number
        )
    )

    await user_mapper.create(user)

    return web.json_response(await auth_user_transformer.transform(user))


async def logout_user(request, user_mapper):
    user = await user_mapper.find(request.get('user_id'))

    user.token = None

    await user_mapper.update(user)

    return web.json_response({})
