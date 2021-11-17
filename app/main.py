import logging
import pathlib
import sys

import aiohttp_cors
from aiohttp import web

from app.containers import ApplicationContainer
from app.resources import setup_routes


def get_config_path():
    return str(
        (pathlib.Path(__file__).parent.parent / 'config' / 'config.yaml').resolve()
    )


def create_app():
    application_container = ApplicationContainer()
    application_container.config.from_yaml(get_config_path())

    app = web.Application(
        middlewares=[
            application_container.middlewares.request_logger,
            application_container.middlewares.error_handler,
            application_container.middlewares.jwt_middleware(),
            application_container.middlewares.additional_token_checker,
        ]
    )
    app.container = application_container
    setup_routes(app)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

    for route in app.router.routes():
        cors.add(route)

    app.on_startup.append(init_resources)
    app.on_shutdown.append(shutdown_resources)

    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    application_container.application_utils.logger().addHandler(logger_handler)

    return app


async def init_resources(app):
    app.container.gateways.init_resources()


async def shutdown_resources(app):
    app.container.gateways.shutdown_resources()


if __name__ == '__main__':
    app = create_app()

    config = app.container.config

    host = config.app.host()
    port = config.app.port()

    web.run_app(app, host=host, port=port)
