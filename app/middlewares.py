from aiohttp import web
from aiohttp_jwt import JWTMiddleware
from marshmallow import ValidationError

from app.exceptions.application import AppException, DomainException
from app.utils.mapper import EntityNotFound


WHITELIST = [
    r"/login",
    r"/register"
]


async def request_logger(request, handler, logger):
    logger.info(f"{request.method} {request.rel_url}")
    response = await handler(request)
    logger.info(f"{response.text}")
    return response


@web.middleware
async def error_handler(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPError as e:
        return web.json_response({
            'error': str(e),
            'payload': {}
        }, status=e.status_code)
    except ValidationError as e:
        return web.json_response({
            'error': 'Validation error',
            'payload': e.messages
        }, status=400)
    except EntityNotFound as e:
        return web.json_response({
            'error': e.message,
            'payload': e.payload
        }, status=404)
    except DomainException as e:
        return web.json_response({
            'error': e.message,
            'payload': e.payload
        }, status=400)
    except AppException as e:
        return web.json_response({
            'error': e.message,
            'payload': e.payload
        }, status=500)
    except Exception as e:
        return web.json_response({
            'error': str(e),
            'payload': {}
        }, status=500)


def create_jwt_middleware(token_config):
    return JWTMiddleware(
        secret_or_pub_key=token_config['secret'],
        algorithms=token_config['algorithm'],
        request_property="token_payload",
        whitelist=WHITELIST
    )


async def additional_token_checker(request, handler, user_mapper):
    if str(request.rel_url) in WHITELIST:
        return await handler(request)

    payload = request.get('token_payload')
    user_id = payload.get('user_id')
    if user_id is None:
        return web.json_response({
            'error': 'User identifier is missing in payload',
            'payload': {}
        }, status=400)

    user = await user_mapper.get_one_by(id=user_id)
    if user.token is None:
        return web.json_response({
            'error': 'Token has been recalled or user has\'t logged in.',
            'payload': {}
        }, status=400)

    if user.token != get_token(request):
        return web.json_response({
            'error': 'Expired token.',
            'payload': {}
        }, status=400)

    request['user_id'] = user_id
    request['user'] = user

    return await handler(request)


def get_token(request):
    return request.headers.get('Authorization').split()[-1]